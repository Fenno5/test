# coding=utf-8
# Copyright 2022 The Google Research Authors.
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

"""Write supervised training tasks to TFRecord dataset."""

import os
import random
from typing import List, Union

from absl import app
from absl import flags

import tensorflow as tf

from latent_programmer.tasks.deepcoder import deepcoder_dsl as dsl
from latent_programmer.tasks.deepcoder import experiment as exp_module
from latent_programmer.tasks.deepcoder import sample_random


gfile = tf.io.gfile

_NUM_WORK_UNITS = flags.DEFINE_integer(
    'num_work_units', 1, 'Total number of work units.')
_SEED = flags.DEFINE_integer(
    'seed', None, 'Fixed random seed.')

_EXPERIMENT = flags.DEFINE_enum(
    'experiment', 'NONE', [e.name for e in exp_module.Experiment],
    'Kind of experiment (see document for descriptions).')
_SPLIT = flags.DEFINE_enum(
    'split', None, ['train', 'valid', 'test', 'finetune'],
    'Which split of the dataset to generate.')
_NUM_TASKS = flags.DEFINE_integer(
    'num_tasks', 100000, 'Number of tasks to write.')
_NUM_EXAMPLES = flags.DEFINE_integer(
    'num_examples', 5, 'Number of examples per task.')
_MAX_PROGRAM_ARITY = flags.DEFINE_integer(
    'max_program_arity', 2, 'Maximum number of inputs.')

_SAVE_DIR = flags.DEFINE_string(
    'save_dir', '/tmp/decomposition/deepcoder', 'Directory to save results to.')


def _bytes_feature(strs):
  """Returns a bytes_list Feature from a list of strings."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(
      value=[str.encode(s) for s in strs]))


def serialize_entire_program_example(task):
  """Creates a tf.Example message for the entire program."""
  input_variables = task.program.input_variables
  example_inputs_strs = [str(dsl.ProgramState(e.inputs, input_variables))
                         for e in task.examples]
  example_outputs_strs = [dsl.result_to_str(e.output) for e in task.examples]
  feature = {
      'inputs': _bytes_feature(example_inputs_strs),
      'outputs': _bytes_feature(example_outputs_strs),
      'program': _bytes_feature([str(task.program)]),
  }
  # Create a Features message using tf.train.Example.
  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()


def serialize_decomposition_examples(task):
  """Returns tf.Example messages for decomposition.

  The current features correspond to the following values:
    inputs: string representation of program state (including inputs and
      intermediate variables)
    outputs: string representation of desired outputs
    next_part: string representation of desired next intermediate outputs
    program_part: string representation of next statement in program that
      generates the next intermediate outputs

  Args:
    task: a dsl.ProgramTask to turn into multiple decomposed examples.
  """
  input_variables = task.program.input_variables
  example_outputs_strs = [dsl.result_to_str(e.output) for e in task.examples]
  states = [dsl.ProgramState(e.inputs, input_variables) for e in task.examples]
  results = []

  for statement in task.program.statements:
    example_inputs_strs = [str(state) for state in states]
    next_states = [statement.run(state) for state in states]
    next_part = [dsl.result_to_str(next_state.get_output())
                 for next_state in next_states]
    program_part_string = str(statement)
    feature = {
        'inputs': _bytes_feature(example_inputs_strs),
        'outputs': _bytes_feature(example_outputs_strs),
        'next_part': _bytes_feature(next_part),
        'program_part': _bytes_feature([program_part_string]),
    }
    example_proto = tf.train.Example(
        features=tf.train.Features(feature=feature))
    results.append(example_proto.SerializeToString())
    states = next_states

  assert ([state.get_output() for state in states]
          == [e.output for e in task.examples])

  return results


def generate_task_for_experiment(experiment,
                                 is_train):
  """Generates a random task for a given experiment and dataset split."""
  if isinstance(experiment, str):
    experiment = exp_module.Experiment[experiment]

  # Generate random inputs.
  num_inputs = random.randint(1, _MAX_PROGRAM_ARITY.value)
  inputs = sample_random.random_inputs(num_inputs)
  # Generate more input examples (must all be the same length and types).
  example_inputs = [inputs]
  for _ in range(_NUM_EXAMPLES.value - 1):
    example_inputs.append(sample_random.random_inputs_like(inputs))

  # Some tasks require a rejection sampling step to enforce some constraints.
  keep_fn = None

  # Generate program.
  if experiment == exp_module.Experiment.NONE:
    num_statements = random.randint(1, 5)
    operations_pool = dsl.OPERATIONS
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.LENGTH_1_4_TO_5:
    num_statements = random.randint(1, 4) if is_train else 5
    operations_pool = dsl.OPERATIONS
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.LENGTH_4_TO_1_5:
    if is_train:
      num_statements = 4
    else:
      num_statements = random.choice([1, 2, 3, 5])
    operations_pool = dsl.OPERATIONS
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.COMPOSE_DIFFERENT_CONCEPTS:
    num_statements = random.randint(2, 4)
    if is_train:
      operations_pool = random.choice([dsl.FIRST_ORDER_OPERATIONS,
                                       dsl.HIGHER_ORDER_OPERATIONS])
    else:
      operations_pool = dsl.OPERATIONS
      keep_fn = lambda program: (  # pylint: disable=g-long-lambda
          any(s.operation in dsl.FIRST_ORDER_OPERATIONS
              for s in program.statements) and
          any(s.operation in dsl.HIGHER_ORDER_OPERATIONS
              for s in program.statements))
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.SWITCH_CONCEPT_ORDER:
    num_statements = random.randint(2, 4)
    operations_pool = None  # Will be set later in sample_random.random_program.
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.COMPOSE_NEW_OP:
    if is_train:
      if random.random() < 0.25:
        num_statements = 1
        operations_pool = dsl.OPERATIONS_ONLY_SCAN
      else:
        num_statements = random.randint(2, 4)
        operations_pool = dsl.OPERATIONS_NO_SCAN
    else:
      num_statements = random.randint(2, 4)
      operations_pool = dsl.OPERATIONS
      keep_fn = lambda program: (  # pylint: disable=g-long-lambda
          any(s.operation.token == 'Scanl1' for s in program.statements))
    lambdas_pool = dsl.LAMBDAS

  elif experiment == exp_module.Experiment.EXTEND_OP_FUNCTIONALITY:
    num_statements = random.randint(1, 4)
    operations_pool = dsl.OPERATIONS
    lambdas_pool = dsl.LAMBDAS
    # In sample_random.random_statement, we make sure the Scanl1 operation only
    # uses the `-` or `min` lambdas during training.
    if not is_train:
      keep_fn = lambda program: (  # pylint: disable=g-long-lambda
          any(f'Scanl1 {lambda_token}' in str(program)
              for lambda_token in ['+', '*', 'max']))
  else:
    raise ValueError(f'Unhandled experiment: {experiment}')

  program = None
  while program is None or (keep_fn and not keep_fn(program)):
    program = sample_random.random_program(
        example_inputs, num_statements, is_train, experiment,
        operations=operations_pool, lambdas=lambdas_pool)

  example_outputs = [program.run(inputs).get_output()
                     for inputs in example_inputs]
  examples = [dsl.Example(inputs, output)
              for inputs, output in zip(example_inputs, example_outputs)]
  return dsl.ProgramTask(program, examples)


def main(_):
  if _SEED.value is not None:
    random.seed(_SEED.value)

  if not gfile.isdir(_SAVE_DIR.value):
    gfile.makedirs(_SAVE_DIR.value)

  shard_id = 0
  total_shards = 1

  entire_programs_fname = os.path.join(
      _SAVE_DIR.value,
      'entire_programs_{}.tf_records-{:05d}-of-{:05d}'.format(
          _SPLIT.value, shard_id, total_shards))
  decomposition_data_fname = os.path.join(
      _SAVE_DIR.value,
      'decomposition_data_{}.tf_records-{:05d}-of-{:05d}'.format(
          _SPLIT.value, shard_id, total_shards))

  # Write the `tf.Example` observations to the file.
  with tf.io.TFRecordWriter(entire_programs_fname) as entire_programs_writer, \
      tf.io.TFRecordWriter(decomposition_data_fname) as decomposition_data_writer:
    for i in range(_NUM_TASKS.value):
      if _SPLIT.value in ['train', 'valid']:
        is_train = True
      elif _SPLIT.value == 'test':
        is_train = False
      elif _SPLIT.value == 'finetune':
        is_train = bool(i % 2)
      else:
        raise ValueError('Unhandled split: {}'.format(_SPLIT.value))
      task = generate_task_for_experiment(_EXPERIMENT.value, is_train)

      entire_programs_writer.write(serialize_entire_program_example(task))
      for example in serialize_decomposition_examples(task):
        decomposition_data_writer.write(example)

if __name__ == '__main__':
  app.run(main)
