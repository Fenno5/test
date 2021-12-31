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

python3 -m venv lfnr
source ./lfnr/bin/activate

pip install -r light_field_neural_rendering/requirements.txt
pip install "jax[cuda110]==0.2.19" -f https://storage.googleapis.com/jax-releases/jax_releases.html

# Run train
python -m light_field_neural_rendering.main --ml_config=light_field_neural_rendering/configs/dev_run.py --workdir=/tmp/test_lfnr --is_train=True
# Run test
python -m light_field_neural_rendering.main --ml_config=light_field_neural_rendering/configs/dev_run.py --workdir=/tmp/test_lfnr --is_train=False
