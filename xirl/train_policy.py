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

"""Launch script for training RL policies with pretrained reward models."""

import collections
import os.path as osp
import logging

import gym
import numpy as np
import torch
import tqdm
from absl import app, flags
from ml_collections import config_flags
from torch.utils.tensorboard import SummaryWriter

from sac import agent, replay_buffer

import utils
from torchkit import checkpoint
from torchkit import Logger
from torchkit.experiment import seed_rngs, set_cudnn
from torchkit.utils.py_utils import Stopwatch

FLAGS = flags.FLAGS

flags.DEFINE_string("experiment_name", None, "Experiment name.")
flags.DEFINE_string("embodiment", None, "The agent embodiment.")
flags.DEFINE_integer("seed", 0, "RNG seed.")
flags.DEFINE_string("device", "cuda:0", "The compute device.")
flags.DEFINE_boolean("resume", False,
                     "Resume experiment from latest checkpoint.")

config_flags.DEFINE_config_file(
    "config",
    "configs/rl_default.py",
    "File path to the training hyperparameter configuration.",
)

flags.mark_flag_as_required("experiment_name")
flags.mark_flag_as_required("embodiment")


def evaluate(
    env: gym.Env,
    policy: agent.SAC,
    logger: SummaryWriter,
    step: int,
) -> None:
  """Evaluate the policy and dump rollout videos to disk."""
  policy.eval()
  eval_stats = collections.defaultdict(list)
  for episode in range(FLAGS.config.num_eval_episodes):
    observation = env.reset()
    while True:
      action = policy.act(observation, sample=False)
      observation, _, done, info = env.step(action)
      if done:
        for k, v in info["metrics"].items():
          eval_stats[k].append(v)
        break
  for k, v in eval_stats.items():
    logger.add_scalar(f"evaluation/{k}s", np.mean(v), step)


def main(_):
  exp_dir = osp.join(FLAGS.config.save_dir, FLAGS.experiment_name)
  utils.setup_experiment(exp_dir, FLAGS.config, FLAGS.resume)

  # Setup compute device.
  if torch.cuda.is_available():
    device = torch.device(FLAGS.device)
    logging.info(f"Using GPU {torch.cuda.get_device_name(device)}.")  # pylint: disable=logging-format-interpolation
  else:
    logging.info("No GPU found. Falling back to CPU.")
    device = torch.device("cpu")

  # Set RNG seeds.
  if FLAGS.SEED is not None:
    logging.info(f"RL experiment seed: {FLAGS.config.SEED}")  # pylint: disable=logging-format-interpolation
    seed_rngs(FLAGS.config.SEED)
    set_cudnn(FLAGS.config.CUDNN_DETERMINISTIC, FLAGS.config.CUDNN_BENCHMARK)
  else:
    logging.info("No RNG seed has been set for this RL experiment.")

  # Load env.
  env_name = utils.xmagical_embodiment_to_env_name(FLAGS.embodiment)
  env = utils.make_env(
      env_name,
      FLAGS.seed,
      action_repeat=FLAGS.config.action_repeat,
      frame_stack=FLAGS.config.frame_stack,
  )
  eval_env = utils.make_env(
      env_name,
      FLAGS.seed + 42,
      action_repeat=FLAGS.config.action_repeat,
      frame_stack=FLAGS.config.frame_stack,
      save_dir=osp.join(exp_dir, "video", "eval"),
  )

  # Dynamically set observation and action space values.
  FLAGS.config.sac.obs_dim = env.observation_space.shape[0]
  FLAGS.config.sac.action_dim = env.action_space.shape[0]
  FLAGS.config.sac.action_range = [
      float(env.action_space.low.min()),
      float(env.action_space.high.max()),
  ]

  policy = agent.SAC(device, FLAGS.config.sac)

  # TODO(kevin): Load the learned replay buffer if we are using learned rewards.
  buffer = replay_buffer.ReplayBuffer(
      env.observation_space.shape,
      env.action_space.shape,
      FLAGS.config.replay_buffer_capacity,
      device,
  )

  # Create checkpoint manager.
  checkpoint_dir = osp.join(exp_dir, "checkpoints")
  checkpoint_manager = checkpoint.CheckpointManager(
      checkpoint.Checkpoint(model=policy, optimizer=optimizer),
      checkpoint_dir,
      device,
  )

  logger = Logger(osp.join(exp_dir, "tb", str(FLAGS.seed)), FLAGS.resume)

  try:
    start = checkpoint_manager.restore_or_initialize()
    done, info, observation = True, {"metrics": {}}, np.empty(())
    for i in tqdm.tqdm(
        range(start, FLAGS.config.num_train_steps), initial=start):
      if done:
        observation = env.reset()
        done = False
        for k, v in info["metrics"].items():
          logger.add_scalar(f"training/{k}", v, i)

      if i < FLAGS.config.num_seed_steps:
        action = env.action_space.sample()
      else:
        policy.eval()
        action = policy.act(observation, sample=True)
      next_observation, reward, done, info = env.step(action)

      if not done or "TimeLimit.truncated" in info:
        mask = 1.0
      else:
        mask = 0.0

      buffer.insert(observation, action, reward, next_observation, mask)
      observation = next_observation

      if i >= FLAGS.config.num_seed_steps:
        policy.train()
        train_info = policy.update(buffer, i)

        if (i + 1) % FLAGS.config.log_frequency == 0:
          for k, v in train_info.items():
            logger.add_scalar(k, v, i)

        # logger.flush()

      if (i + 1) % FLAGS.config.eval_frequency == 0:
        evaluate(eval_env, policy, logger, i)

      if (i + 1) % FLAGS.config.checkpoint_frequency == 0:
        checkpoint_manager.save(i)

  except KeyboardInterrupt:
    print("Caught keyboard interrupt. Saving before quitting.")

  finally:
    checkpoint_manager.save(i)
    logger.close()


if __name__ == "__main__":
  app.run(main)
