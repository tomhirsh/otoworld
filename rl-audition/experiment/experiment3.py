import sys
sys.path.append("../src/")

import gym
import numpy as np
import matplotlib.pyplot as plt
import torch
import room_types
import agent
import audio_room
import utils
import constants
import nussl
from datasets import BufferData
import time
import audio_processing
from models import RnnAgent
import transforms

"""
Experiment 3 details: 
Train the agent on the actual model which includes separation model + Q Network (The RNNQNet model) 
"""


def run():
    # Shoebox Room
    room = room_types.ShoeBox(x_length=10, y_length=10)

    # Uncomment for Polygon Room
    # room = room_types.Polygon(n=6, r=2, x_center=5, y_center=5)

    agent_loc = np.array([3, 8])

    # Set up the gym environment
    env = gym.make(
        "audio-room-v0",
        room_config=room.generate(),
        agent_loc=agent_loc,
        corners=room.corners,
        max_order=10,
        step_size=1.0,
        acceptable_radius=0.8,
    )

    # create buffer data folders
    utils.create_buffer_data_folders()

    # tfm = nussl.datasets.transforms.Compose([
    #     nussl.datasets.transforms.GetAudio(mix_key='new_state'),
    #     nussl.datasets.transforms.ToSeparationModel(),
    #     nussl.datasets.transforms.GetExcerpt(excerpt_length=32000, tf_keys=['mix_audio'], time_dim=1),
    # ])

    tfm = transforms.Compose([
        transforms.GetAudio(mix_key=['prev_state', 'new_state']),
        transforms.ToSeparationModel(),
        transforms.GetExcerpt(excerpt_length=32000,
                              tf_keys=['mix_audio_prev_state', 'mix_audio_new_state'], time_dim=1),
    ])

    # create dataset object (subclass of nussl.datasets.BaseDataset)
    dataset = BufferData(folder=constants.DIR_DATASET_ITEMS, to_disk=False, transform=tfm)

    # Define the relevant dictionaries
    env_config = {'env': env, 'dataset': dataset, 'episodes': 3, 'max_steps': 250, 'plot_reward_vs_steps': False,
                  'stable_update_freq': 3, 'epsilon': 0.7, 'save_freq': 1}
    dataset_config = {'batch_size': 25, 'num_updates': 2, 'save_path': '../models/'}
    rnn_agent = RnnAgent(env_config=env_config, dataset_config=dataset_config)

    print('Fitting rnn agent')
    rnn_agent.fit()


if __name__ == '__main__':
    run()
