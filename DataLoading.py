"""
 function to open an OEphys data file, and return continuous uV data from specified channels

Usage:
import DataLoading as DL
data = DL.load_data('<filename>',[<channel array>])
"""
# import package dependency from OEPhys team (https://github.com/open-ephys/open-ephys-python-tools)
from open_ephys.analysis import Session
import numpy as np
import os


def load_data(folder, channels):
    # point loading engine to relevant data file
    folder = os.path.join('/home/mccaffertylab/Documents/Neural Data (Live)', folder)
    session = Session(folder)  # import datafile into memory mapped object
    # extract continuous data into separate variable
    data_mem_map = session.recordnodes[0].recordings[0].continuous[0].samples

    #  Extract the conversion factor between the stored int16 values and true uV
    bit_volt = session.recordnodes[0].recordings[0].info['continuous']
    bit_volt = bit_volt[0]
    bit_volt = bit_volt['channels']
    bit_volt = bit_volt[0]
    bit_volt = bit_volt['bit_volts']

    chanmap = np.array([1, 4, 7, 3, 0, 5, 15, 2, 8, 6, 14, 9, 13, 10, 12, 11, 16])   # create channel mapping
    channels = chanmap[channels]  # restrict data extraction to requested channels
    # convert memory mapped array into nd array and convert into uV values
    data = data_mem_map[:, channels] * bit_volt

    return data
