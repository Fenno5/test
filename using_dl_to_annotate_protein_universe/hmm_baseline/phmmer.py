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

r"""Run PHMMer and get predictions vs actual family membership.

Given fasta files of unaligned amino acid sequences in a training file,
and fasta files of unaligned amino acid sequences in a test directory,
compute a prediction for the class membership of each sequence in the test
directory. These fasta files are generated by generate_hmmer_files.py.

The way that prediction of classes is determined is by a process similar to
1-nearest-neighbors.

PHMMer can be installed by running apt-get install hmmer.

The HMMER manual can be found at
http://eddylab.org/software/hmmer3/3.1b2/Userguide.pdf

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import subprocess

from absl import logging
from Bio.SeqIO import FastaIO
import hmmer_utils
import parallel
import pfam_utils
import tensorflow.compat.v1 as tf

# Optimize the speed of running phmmer.
_BLOCK_SIZE = 131
_CPUS = 9
_THREADS = 8


def run_phmmer_for_query(train_sequence_file,
                         list_of_protein_name_and_sequence):
  """Return output of phmmer binary of one query against all sequences.

  Args:
    train_sequence_file: string. Filename of fasta file of training sequences.
    list_of_protein_name_and_sequence: list of tuples of (protein_name,
      sequence).
      The protein_name: string. Of the form `sequence_name`_`family_accession`,
        like OLF1_CHICK/41-290_PF00001.20.
      The sequence: string. Amino acid sequence corresponding to protein_name.

  Returns:
    List of HMMEROutputs. Output of running the binary phmmer.
  """

  protein_name_and_sequence_as_fasta_list = [
      '>{}\n{}'.format(protein_name, sequence)
      for protein_name, sequence in list_of_protein_name_and_sequence
  ]
  protein_name_and_sequence_formatted = '\n'.join(
      protein_name_and_sequence_as_fasta_list)

  # Here we discard the normal stdout of phmmer with -o /dev/null, as we don't
  # use it. Then redirect the normal file output from phmmer to /dev/stdout to
  # avoid making a file and reading it back in for parsing. This allows us to
  # immediately treat it as a python string.
  # Use the stdin option for phmmer by using the filename '-'. Then, use
  # p.communicate to send the process the input fasta strings.
  p = subprocess.Popen(
      (('phmmer --tblout /dev/stdout -o /dev/null -E 10.0  --cpu={cpus} - '
        '{train_sequence_file}').format(
            cpus=_CPUS, train_sequence_file=train_sequence_file)).split(),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
  stdout, stderr = p.communicate(protein_name_and_sequence_formatted)
  if stderr:
    logging.warning('phmmer returned an error for sequences %s: %s',
                    protein_name_and_sequence_formatted, stderr)
  all_query_identifiers = set(
      protein_name for protein_name, _ in list_of_protein_name_and_sequence)
  return hmmer_utils.parse_phmmer_output(
      stdout, query_identifiers=all_query_identifiers)


def write_phmmer_predictions(train_sequence_file, test_sequence_file,
                             parsed_output):
  """Write prediction csv file for all files in test_sequence_dir.

  The csv content is:
  sequence_name,true_label,predicted_label

  Where sequence_name is the uniprot identifier, including domain indices,
  and true and predicted label are pfam family accession ids.

  Args:
    train_sequence_file: string. Filename of fasta file of unaligned training
      sequences.
    test_sequence_file: string. Fasta files of unaligned test sequences.
    parsed_output: string. csv file for parsed phmmer outputs.
  """
  logging.info('Writing predictions to %s', parsed_output)

  with tf.io.gfile.GFile(test_sequence_file, 'r') as input_file:
    batched_fasta_iterable = pfam_utils.batch_iterable(
        FastaIO.SimpleFastaParser(input_file), _BLOCK_SIZE)

    input_dict_to_phmmer_function = [
        dict(
            train_sequence_file=train_sequence_file,
            list_of_protein_name_and_sequence=list_of_protein_name_and_sequence)
        for list_of_protein_name_and_sequence in batched_fasta_iterable
    ]

  results = parallel.RunInParallel(
      run_phmmer_for_query,
      input_dict_to_phmmer_function,
      _THREADS,
      cancel_futures=True)

  with tf.io.gfile.GFile(parsed_output, 'w') as parsed_output_file:
    for phmmer_query_result in results:
      for phmmer_output in phmmer_query_result:
        parsed_output_file.write(phmmer_output.format_as_csv() + '\n')
