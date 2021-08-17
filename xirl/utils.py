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

import functools
import math
import random
import numpy as np
import subprocess
import typing
import os

import gym
import torch
from ml_collections import ConfigDict

from sac import wrappers
from xirl import common
import xmagical

from gym.wrappers import RescaleAction

# ========================================= #
# General utils.
# ========================================= #


def git_revision_hash() -> str:
  """Return git revision hash as a string.
  
  Reference: https://stackoverflow.com/a/21901260
  """
  return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()


def seed_rngs(seed: int):
  """Seeds python, numpy, and torch RNGs."""
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)


def set_cudnn(deterministic: bool = False, benchmark: bool = True):
  """Set PyTorch-related CUDNN settings."""
  torch.backends.cudnn.deterministic = deterministic
  torch.backends.cudnn.benchmark = benchmark


# ========================================= #
# RL utils.
# ========================================= #

def xmagical_embodiment_to_env_name(embodiment: str) -> str:
  VALID_EMBS = ["shortstick", "mediumstick", "longstick", "gripper"]
  if embodiment not in VALID_EMBS:
    raise ValueError(f"Valid embodiments are: {VALID_EMBS}")
  # We used the TestLayout variant for the paper.
  return f"SweepToTop-{embodiment.capitalize()}-State-Allo-TestLayout-v0"


def make_env(
  env_name: str,
  seed: int,
  save_dir: typing.Optional[str] = None,
  add_episode_monitor: bool = True,
  action_repeat: int = 1,
  frame_stack: int = 1,
) -> gym.Env:
  """Env factory with wrapping.
  
  Args:
    env_name:
    seed:
    save_dir:
    add_episode_monitor:
    action_repeat:
    frame_stack:
  """
  # Check if the env is in x-magical.
  xmagical.register_envs()
  if env_name in xmagical.ALL_REGISTERED_ENVS:
    env = gym.make(env_name)
  else:  # Check the RLV envs.
    raise ValueError("RLV env not yet supported.")

  if add_episode_monitor:
    env = wrappers.EpisodeMonitor(env)
  if action_repeat > 1:
    env = wrappers.ActionRepeat(env, action_repeat)
  env = RescaleAction(env, -1.0, 1.0)
  if save_dir is not None:
    env = wrappers.VideoRecorder(env, save_dir=save_dir)
  if frame_stack > 1:
    env = wrappers.FrameStack(env, frame_stack)

  # Seed.
  env.seed(seed)
  env.action_space.seed(seed)
  env.observation_space.seed(seed)

  return env


def wrap_learned_reward(
  env: gym.Env,
  pretrained_path: str,
  rl_config: ConfigDict,
  device: torch.device,
) -> gym.Env:
  """Learned reward wrapper.
  
  Args:
    env:
    pretrained_path:
    rl_config:
    device:
  """
  model_config, model = common.load_model_checkpoint(
    pretrained_path,
    device=device,
  )

  kwargs = {
      "env": env,
      "model": model,
      "device": device,
      "res_hw": model_config.DATA_AUGMENTATION.IMAGE_SIZE,
  }

  if rl_config.reward_wrapper.type == "goal_classifier":
    env = wrappers.GoalClassifierVisualReward(**kwargs)

  elif rl_config.reward_wrapper.type == "distance_to_goal":
    kwargs["goal_emb"] = common.load_goal_embedding(pretrained_path)
    kwargs["distance_scale"] = rl_config.reward_wrapper.distance_scale
    if rl_config.reward_wrapper.distance_func == "sigmoid":
      def sigmoid(x, t = 1.0):
        return 1 / (1 + math.exp(-x / t))

      kwargs["distance_func"] = functools.partial(
          sigmoid,
          rl_config.reward_wrapper.distance_func_temperature,
      )
    env = wrappers.DistanceToGoalVisualReward(**kwargs)

  else:
    raise ValueError(f"{rl_config.reward_wrapper.type} is not a valid reward wrapper.")

  return env
