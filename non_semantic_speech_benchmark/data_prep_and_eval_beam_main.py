# coding=utf-8
# Copyright 2021 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint:disable=line-too-long
r"""For a given dataset, prep dataset and run sklearn eval.

This file has two modes:
1) Map from tf.Examples of audio to tf.Examples of embeddings.
2) Map from TFDS dataseet to tf.Examples of embeddings.

"""
# pylint:enable=line-too-long

from typing import Sequence
from absl import app
from absl import flags
from absl import logging
import apache_beam as beam
import tensorflow as tf


# Gets flags from data_prep's main.
from non_semantic_speech_benchmark.data_prep import audio_to_embeddings_beam_main as data_prep  # pylint:disable=unused-import
from non_semantic_speech_benchmark.data_prep import audio_to_embeddings_beam_utils as data_prep_utils
from non_semantic_speech_benchmark.eval_embedding.sklearn import train_and_eval_sklearn as sklearn_utils

# Flags needed for data prep. Data prep flags are imported directly from the
# main data prep beam file, but we need some custom behavior. XOR with
# tfds_dataset.
flags.DEFINE_string('train_input_glob', None, 'Glob for training data.')
flags.DEFINE_string('validation_input_glob', None, 'Glob for validation data.')
flags.DEFINE_string('test_input_glob', None, 'Glob for test data.')
flags.DEFINE_bool('skip_existing_error', False, 'Skip existing errors.')

# Flags needed for sklearn eval.
flags.DEFINE_string('results_output_file', None, 'Output filename.')
flags.DEFINE_list('label_list', None, 'Python list of possible label values.')
flags.DEFINE_enum('eval_metric', 'accuracy', [
    'accuracy', 'balanced_accuracy', 'equal_error_rate',
    'unweighted_average_recall', 'auc'
], 'Which metric to compute and report.')

FLAGS = flags.FLAGS


def main(unused_argv):

  # Data prep setup.
  run_data_prep = True
  if FLAGS.train_input_glob:
    assert FLAGS.validation_input_glob
    assert FLAGS.test_input_glob
    input_filenames_list, output_filenames = [], []
    for input_glob in [
        FLAGS.train_input_glob, FLAGS.validation_input_glob,
        FLAGS.test_input_glob,
    ]:
      FLAGS.input_glob = input_glob
      cur_inputs, cur_outputs, beam_params = data_prep_utils.get_beam_params_from_flags(
      )
      input_filenames_list.extend(cur_inputs)
      output_filenames.extend(cur_outputs)
  else:
    input_filenames_list, output_filenames, beam_params = data_prep_utils.get_beam_params_from_flags(
    )
  assert input_filenames_list, input_filenames_list
  assert output_filenames, output_filenames
  try:
    # Check that inputs and flags are formatted correctly.
    data_prep_utils.validate_inputs(
        input_filenames_list, output_filenames,
        beam_params['embedding_modules'], beam_params['embedding_names'],
        beam_params['module_output_keys'])
  except ValueError:
    if FLAGS.skip_existing_error:
      run_data_prep = False
    else:
      raise
  logging.info('beam_params: %s', beam_params)

  # Generate sklearn eval experiment parameters based on data prep flags.
  if len(output_filenames) != 3:
    raise ValueError(f'Data prep output must be 3 files: {output_filenames}')
  # Make them globs.
  train_glob, eval_glob, test_glob = [f'{x}*' for x in output_filenames]
  sklearn_results_output_file = FLAGS.results_output_file
  exp_params = sklearn_utils.experiment_params(
      embedding_list=beam_params['embedding_names'],
      speaker_id_name=FLAGS.speaker_id_key,
      label_name=FLAGS.label_key,
      label_list=FLAGS.label_list,
      train_glob=train_glob,
      eval_glob=eval_glob,
      test_glob=test_glob,
      save_model_dir=None,
      save_predictions_dir=None,
      eval_metric=FLAGS.eval_metric,
  )
  logging.info('exp_params: %s', exp_params)

  # Make and run beam pipeline.
  beam_options = None

  if run_data_prep:
    logging.info('Data prep on: %s, %s...', input_filenames_list,
                 output_filenames)
    with beam.Pipeline(beam_options) as root:
      for i, (input_filenames_or_glob, output_filename) in enumerate(
          zip(input_filenames_list, output_filenames)):
        data_prep_utils.make_beam_pipeline(
            root,
            input_filenames=input_filenames_or_glob,
            output_filename=output_filename,
            suffix=str(i),
            **beam_params)

  # Check that previous beam pipeline wrote outputs.
  sklearn_utils.validate_flags(train_glob, eval_glob, test_glob,
                               sklearn_results_output_file)
  logging.info('Eval sklearn...')
  with beam.Pipeline(beam_options) as root:
    _ = (
        root
        | 'MakeCollection' >> beam.Create(exp_params)
        | 'CalcScores' >> beam.Map(
            lambda d: (d, sklearn_utils.train_and_get_score(**d)))
        | 'FormatText' >> beam.Map(sklearn_utils.format_text_line)
        | 'Reshuffle' >> beam.Reshuffle()
        | 'WriteOutput' >> beam.io.WriteToText(
            sklearn_results_output_file, num_shards=1))


if __name__ == '__main__':
  # From data prep.
  flags.mark_flags_as_required([
      'output_filename',
      'embedding_names',
      'embedding_modules',
      'module_output_keys',
      'audio_key',
  ])
  flags.mark_flags_as_mutual_exclusive(['train_input_glob', 'tfds_dataset'],
                                       required=True)
  flags.mark_flags_as_mutual_exclusive(
      ['validation_input_glob', 'tfds_dataset'], required=True)
  flags.mark_flags_as_mutual_exclusive(['test_input_glob', 'tfds_dataset'],
                                       required=True)
  flags.mark_flags_as_mutual_exclusive(
      ['tfds_dataset', 'sample_rate_key', 'sample_rate'], required=True)
  assert tf.executing_eagerly()

  # From sklearn eval.
  flags.mark_flags_as_required([
      'label_key',
      'label_list',
      'results_output_file',
  ])
  app.run(main)
