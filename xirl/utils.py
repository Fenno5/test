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

"""Useful methods shared by all scripts."""

from typing import Any, Dict, Optional

import os
import matplotlib.pyplot as plt
import yaml
import uuid
import numpy as np
import typing
import pickle
from torchkit import checkpoint
from torchkit.experiment import git_revision_hash
import gym
import torch
from ml_collections import config_dict
from sac import wrappers
from xirl import common
import xmagical
from gym.wrappers import RescaleAction

ConfigDict = config_dict.ConfigDict
FrozenConfigDict = config_dict.FrozenConfigDict

# ========================================= #
# Experiment utils.
# ========================================= #


def setup_experiment(exp_dir: str, config: ConfigDict, resume: bool = False):
  """Initializes a pretraining or RL experiment.

  If the experiment directory doesn't exist yet, creates it and dumps the config
  dict as a yaml file and git hash as a text file. If it exists already, raises
  a ValueError to prevent overwriting unless resume is set to True.
  """
  if os.path.exists(exp_dir):
    if not resume:
      raise ValueError(
          "Experiment already exists. Run with --resume to continue.")
    load_config_from_dir(exp_dir, config)
  else:
    os.makedirs(exp_dir)
    with open(os.path.join(exp_dir, "config.yaml"), "w") as fp:
      yaml.dump(ConfigDict.to_dict(config), fp)
    with open(os.path.join(exp_dir, "git_hash.txt"), "w") as fp:
      fp.write(git_revision_hash())


def load_config_from_dir(
    exp_dir: str,
    config: Optional[ConfigDict] = None,
) -> Optional[ConfigDict]:
  """Load experiment config."""
  try:
    with open(os.path.join(exp_dir, "config.yaml"), "r") as fp:
      cfg = yaml.load(fp, Loader=yaml.FullLoader)
    # Inplace update the config if one is provided.
    if config is not None:
      config.update(cfg)
      return
    return ConfigDict(cfg)
  except FileNotFoundError as e:
    raise e


def dump_config(exp_dir: str, config: ConfigDict):
  """Dump config to disk."""
  # Note: No need to explicitly delete the previous config file as "w" will
  # overwrite the file if it already exists.
  with open(os.path.join(exp_dir, "config.yaml"), "w") as fp:
    yaml.dump(ConfigDict.to_dict(config), fp)


def copy_config_and_replace(
    config: ConfigDict,
    update_dict: Optional[Dict[str, Any]] = None,
    freeze: bool = False,
) -> ConfigDict:
  """Makes a copy of a config and optionally updates its values."""
  # Using the ConfigDict constructor leaves the `FieldReferences` untouched
  # unlike `ConfigDict.copy_and_resolve_references`.
  new_config = ConfigDict(config)
  if update_dict is not None:
    new_config.update(update_dict)
  if freeze:
    return FrozenConfigDict(new_config)
  return new_config


def load_model_checkpoint(
    pretrained_path: str,
    device: torch.device,
):
  """Load a pretrained model and optionally a precomputed goal embedding."""
  config = load_config_from_dir(pretrained_path)
  model = common.get_model(config)
  checkpoint_dir = os.path.join(pretrained_path, "checkpoints")
  checkpoint_manager = checkpoint.CheckpointManager(
      checkpoint.Checkpoint(model=model), checkpoint_dir, device)
  global_step = checkpoint_manager.restore_or_initialize()
  print(f"Restored model from checkpoint @{global_step}.")
  return config, model


def load_goal_embedding(pretrained_path: str) -> Optional[np.ndarray]:
  """Load a pickled goal embedding."""
  try:
    with open(os.path.join(pretrained_path, "goal_emb.pkl"), "rb") as fp:
      goal_emb = pickle.load(fp)
    print("Successfully loaded goal embedding.")
    return goal_emb
  except FileNotFoundError as e:
    raise e


# ========================================= #
# RL utils.
# ========================================= #


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
    env_name: The name of the environment.
    seed: The RNG seed.
    save_dir: Specifiy a save directory to wrap with `VideoRecorder`.
    add_episode_monitor: Set to True to wrap with `EpisodeMonitor`.
    action_repeat: A value > 1 will wrap with `ActionRepeat`.
    frame_stack: A value > 1 will wrap with `FrameStack`.
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
) -> gym.Env:
  """Wrap the environment with a learned reward wrapper.

  Args:
    env: A `gym.Env` to wrap with a `LearnedVisualRewardWrapper` wrapper.
    pretrained_path: Path to a pretrained `xirl.models.SelfSupervisedModel`.
    rl_config:
  """
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model_config, model = load_model_checkpoint(pretrained_path, device)

  kwargs = {
      "env": env,
      "model": model,
      "device": device,
      "res_hw": model_config.DATA_AUGMENTATION.IMAGE_SIZE,
  }

  if rl_config.reward_wrapper.type == "goal_classifier":
    env = wrappers.GoalClassifierLearnedVisualReward(**kwargs)

  elif rl_config.reward_wrapper.type == "distance_to_goal":
    kwargs["goal_emb"] = load_goal_embedding(pretrained_path)
    kwargs["distance_scale"] = rl_config.reward_wrapper.distance_scale
    env = wrappers.DistanceToGoalLearnedVisualReward(**kwargs)

  else:
    raise ValueError(
        f"{rl_config.reward_wrapper.type} is not a valid reward wrapper.")

  return env


# ========================================= #
# Misc. utils.
# ========================================= #


def plot_reward(rews: typing.Sequence[float]):
  """Plot raw and cumulative rewards over an episode."""
  _, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True)
  axes[0].plot(rews)
  axes[0].set_xlabel("Timestep")
  axes[0].set_ylabel("Reward")
  axes[1].plot(np.cumsum(rews))
  axes[1].set_xlabel("Timestep")
  axes[1].set_ylabel("Cumulative Reward")
  for ax in axes:
    ax.grid(b=True, which="major", linestyle="-")
    ax.grid(b=True, which="minor", linestyle="-", alpha=0.2)
  plt.minorticks_on()
  plt.show()


def string_from_kwargs(**kwargs) -> str:
  return "_".join([f"{k}={v}" for k, v in kwargs.items()])


def unique_id() -> str:
  """Generate a unique ID as specified in RFC 4122."""
  # See https://docs.python.org/3/library/uuid.html
  return str(uuid.uuid4())
