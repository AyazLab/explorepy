# An example code for impedance data acquisition from Explore device
import csv
import signal
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import explorepy
from explorepy.stream_processor import TOPICS


EXG_CHANNELS = [f"ch{i}" for i in range(1, 32 + 1)]
file_obj = open('exg_data_imp_mode.csv', 'w', newline='\n')
csv_obj = csv.writer(file_obj, delimiter=",")
csv_obj.writerow(['TimeStamp'] + EXG_CHANNELS[:8])

def _process_packet_data(packet):
    """Helper function to extract and format data from a packet."""
    time_vector, sig = packet.get_data(250)
    data = np.concatenate((np.array(time_vector)[:, np.newaxis].T, np.array(sig)), axis=0)
    data = np.round(data, 4)
    np.savetxt(file_obj, data.T, fmt='%4f', delimiter=',')

def handle_exg(packet):
    print('#######################')
    _process_packet_data(packet)

def handle_imp(packet):
    """A function that receives impedance packet values"""
    imp_values = packet.get_impedances()
    print('IMP: ******************')
    print(imp_values)



exp_device = explorepy.Explore()
exp_device.connect('Explore_AAXX')
exp_device.stream_processor.subscribe(callback=handle_imp, topic=TOPICS.imp)
exp_device.stream_processor.subscribe(callback=handle_exg, topic=TOPICS.raw_ExG)

# enable impedance mode
exp_device.stream_processor.imp_initialize(notch_freq=50)

count = 0
while count < 40:
    time.sleep(1)
    count += 1

exp_device.stream_processor.disable_imp()
exp_device.stream_processor.unsubscribe(callback=handle_imp, topic=TOPICS.imp)
exp_device.stream_processor.unsubscribe(callback=handle_exg, topic=TOPICS.raw_ExG)
file_obj.close()




