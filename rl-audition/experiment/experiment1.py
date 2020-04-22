import sys
sys.path.append("../src/")  # get modules from src folder

import gym
import numpy as np
import matplotlib.pyplot as plt

import room_types
import agent
import audio_room
import utils
import constants
from datasets import BufferData


def run_random_agent():
    # paths of audio files
    paths = utils.choose_random_files()

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
        direct_sources=paths,
        acceptable_radius=0.8,
    )
    env.add_sources()

    # create buffer data folders
    utils.create_buffer_data_folders()

    # create dataset object (subclass of nussl.datasets.BaseDataset)
    dataset = BufferData(folder=constants.DIR_DATASET_ITEMS, to_disk=True)

    # Load the agent class
    a = agent.RandomAgent(env=env, dataset=dataset, episodes=10, steps=1000)
    a.fit()


if __name__ == "__main__":
    run_random_agent()
