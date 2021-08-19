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

#!/bin/bash
set -e
set -x

python pretrain.py \
    --experiment_name='testingtcc2' \
    --config=experiments/xmagical/pretraining/tcc.py \
    --config.OPTIM.TRAIN_MAX_ITERS=25 \
    --config.FRAME_SAMPLER.NUM_FRAMES_PER_SEQUENCE=3

python interact_reward.py \
  --config.reward_wrapper.pretrained_path=/tmp/xirl/pretrain_runs/test \
  --config.reward_wrapper.distance_scale=0.01
