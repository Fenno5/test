# coding=utf-8
# Copyright 2023 The Google Research Authors.
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

r"""This script aggregates class level performance metrics.

This script imports a csv generated by aggregate_ckpt_metrics.py.
These metrics are used to compute a class level t-statistic.


"""

import os
import time

from absl import app
from absl import flags
import pandas as pd
from scipy.stats import ttest_ind
import tensorflow.compat.v1 as tf

from pruning_identified_exemplars.utils import class_level_metrics

FLAGS = flags.FLAGS

flags.DEFINE_enum('mode', 'eval', ('eval', 'train'),
                  'Mode designated as train or eval.')
flags.DEFINE_string('output_file', '', 'File to save the csv data to.')
flags.DEFINE_float('sparsity_fraction', 0.1, 'Fraction pruned.')
flags.DEFINE_string('data_directory', '', 'File to read data from.')

# mean accuracy across 30 models trained to different levels of sparsity.
imagenet_params = {
    'accuracy': {
        0.0: 0.76675,
        0.1: 0.76662,
        0.3: 0.76459,
        0.5: 0.75874,
        0.7: 0.75019,
        0.9: 0.72569
    },
    'num_classes': 1000,
}


def generate_tstats_classes(df, dest_dir, params):
  """Computes t-test for each class.

   This function computes a t-test for each class in the dataset.
   The t-test is computed by comparing class level metrics for
   a set of sparse model checkpoints to non-sparse model
   checkppints.

  Args:
    df: input dataframe with class level metrics.
    dest_dir: pathway to output directory.
    params: dataset specific params.
  """

  human_label_lookup = class_level_metrics.HumanLabelLookup()
  label_dict = human_label_lookup.create_library()
  class_names = list(label_dict.values())

  df.drop(columns='Unnamed: 0')
  df.reset_index(inplace=True, drop=True)
  df['id'] = df.index

  df_ = pd.wide_to_long(
      df,
      stubnames=['precision', 'recall'],
      i='id',
      j='class',
      sep='/',
      suffix=r'\w+').reset_index()

  data = pd.DataFrame([])

  num_classes = params['num_classes']
  mean_accuracy_dict = params['accuracy']

  long_df_all = df_
  for i in range(num_classes):

    # adding label id ensures unique naming of classes
    c = class_names[i] + '_' + str(i)
    for p in [0.1, 0.3, 0.5, 0.7, 0.9]:

      variant_mean_recall = long_df_all[(
          (long_df_all['fraction_pruned'] == p) &
          (long_df_all['class'] == c))]['recall'].mean()

      baseline_mean_recall = long_df_all[(
          (long_df_all['fraction_pruned'] == 0.0) &
          (long_df_all['class'] == c))]['recall'].mean()

      # normalize recall by model accuracy
      baseline_set = long_df_all[(
          (long_df_all['fraction_pruned'] == 0.0) &
          (long_df_all['class'] == c))]['recall'] - mean_accuracy_dict[0.0]
      variant_set = long_df_all[(
          (long_df_all['fraction_pruned'] == p) &
          (long_df_all['class'] == c))]['recall'] - mean_accuracy_dict[p]

      t_stat = ttest_ind(baseline_set, variant_set, equal_var=False)

      data = data.append(
          pd.DataFrame(
              {
                  'class': c,
                  'pruning_fraction': p,
                  'baseline_mean_recall': baseline_mean_recall,
                  'variant_mean_recall': variant_mean_recall,
                  'pvalue_recall_norm': t_stat[1],
                  'statistic_recall_norm': t_stat[0],
              },
              index=[0]),
          ignore_index=True)

  time_ = str(time.time())
  output_file = 'recall_t_statistic'
  file_name = '_' + time_ + '_' + output_file + '.csv'
  file_path = os.path.join(dest_dir, file_name)
  with tf.gfile.Open(file_path, 'w') as f:
    data.to_csv(f)


def read_all_eval_subdir(data_directory):
  """Aggregate metrics across shards.

  Args:
    data_directory: pathway to class level metrics csv.

  Returns:
    A pandas dataframe with all imported records.
  """

  filenames = tf.gfile.Glob(data_directory + '/' + '*.csv')

  df = []
  for filename in filenames:
    with tf.gfile.Open(filename) as f:
      df_ = pd.read_csv(f)
      df.append(df_)

  df_ = pd.concat(df, ignore_index=False)
  return df_


def main(argv):
  del argv  # Unused.

  params = imagenet_params

  dest_dir = os.path.join(FLAGS.output_file, 'imagenet', FLAGS.mode)

  df = read_all_eval_subdir(data_directory=FLAGS.data_directory)

  generate_tstats_classes(df=df, dest_dir=dest_dir, params=params)


if __name__ == '__main__':
  app.run(main)
