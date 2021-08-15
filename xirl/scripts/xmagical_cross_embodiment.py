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

"""Section V.B: Learning from Cross-Embodiment Demonstrations, Fig 5."""

import os.path as osp
import random
import subprocess
from absl import app
from absl import flags

# The supported pretraining algorithms.
ALGORITHMS = ["xirl", "tcn", "lifs", "goal_classifier", "raw_imagenet"]
# The embodiment classes in the dataset.
EMBODIMENTS = ["longstick", "mediumstick", "shortstick", "gripper"]
# Mapping from pretraining algorithm to config file.
ALGO_TO_CONFIG = {
    "xirl": "experiments/xmagical/pretraining/tcc.py",
    "lifs": "experiments/xmagical/pretraining/lifs.py",
    "tcn": "experiments/xmagical/pretraining/tcn.py",
    "goal_classifier": "experiments/xmagical/pretraining/classifier.py",
    "raw_imagenet": "experiments/xmagical/pretraining/imagenet.py",
}
# We want to pretrain on the entire 1k demonstrations.
MAX_DEMONSTRATIONS = -1

FLAGS = flags.FLAGS
flags.DEFINE_enum("algo", None, ALGORITHMS, "The pretraining algorithm to use.")
flags.mark_flag_as_required("algo")


def main(_):
  for embodiment in EMBODIMENTS:
    # Generate a unique experiment name.
    experiment_name = "exp2_algo={}_embodiment={}_maxdemos={}_uid={}".format(
        FLAGS.algo, embodiment, MAX_DEMONSTRATIONS, int(random.random() * 1e9))
    print(f"Experiment name: {experiment_name}")

    # Train on all classes but the given embodiment.
    trainable_embs = tuple(set(EMBODIMENTS) - set([embodiment]))

    subprocess.call([
        "python",
        "pretrain.py",
        "--experiment_name",
        experiment_name,
        "--raw_imagenet" if FLAGS.algo == "raw_imagenet" else '',
        "--config",
        f"{ALGO_TO_CONFIG[FLAGS.algo]}",
        "--config.DATA.PRETRAIN_ACTION_CLASS",
        f"{repr(trainable_embs)}",
        "--config.DATA.DOWNSTREAM_ACTION_CLASS",
        f"{repr(trainable_embs)}",
        "--config.DATA.MAX_VIDS_PER_CLASS",
        f"{MAX_DEMONSTRATIONS}",
    ])

    # The 'goal_classifier' baseline does not need to compute a goal embedding.
    if FLAGS.algo != "goal_classifier":
      subprocess.call([
          "python",
          "compute_goal_embedding.py",
          "--experiment_path",
          # Note: This assumes that the config.ROOT_DIR value has not been
          # changed to its default value of 'tmp/xirl'.
          osp.join("/tmp/xirl", experiment_name),
      ])


if __name__ == "__main__":
  app.run(main)
