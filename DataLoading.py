"""

Some helper functions for loading in continuous OEPhys data, applying a filter...

Usage:
import DataLoading as DL
data = DL.load_data('<filename>',[<channel array>])
"""
# import package dependency from OEPhys team (https://github.com/open-ephys/open-ephys-python-tools)
from open_ephys.analysis import Session
from scipy import signal
import numpy as np
import os


def load_data(folder, channels):
    """
    function to open an OEphys data file, and return continuous uV data from specified channels
    :param folder:
    :param channels:
    :return:
    """
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


def ButterFilt(data,low_corner,high_corner, fs)
    """
    function to design and implement a 4th order Butterworth Bandpass filter, and run it over a data matrix forward & backward
    
    :param data: ndarray
                matrix of time-series data
    :param low_corner: int
                        frequency (Hz) of low cut-off frequency
    :param high_corner: int
                        frequency (Hz) of high cut-off frequency
    :param fs: int
                Sample frequency of data (Hz)
    :return: ndarray
                Filtered time-series data
    """

    wn = np.array([low_corner, high_corner]) #create corner frequency array
    sos = signal.butter(2,wn,btype='bandpass',output='sos',fs=fs) #compute sos coefficients for filter
    filt_data= signal.sosfiltfilt(sos, data, axis=0) #perform forward and backwards filtering over 1st dimension of data array
    return filt_data
