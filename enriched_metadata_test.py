# -*- coding: utf-8 -*-
import explorepy
from explorepy.BLEClient import BLEClient
from explorepy import settings_manager
import time

# Set the Bluetooth interface to 'mock' to use the mock server
explorepy.set_bt_interface('mock')

# Create an Explore instance and connect (device_name can be any string)
explore = explorepy.Explore()
explore.connect(device_name='Explore_1C35') #Using device n

# Set channel names
explore.set_exg_channel_name(1, 'Pz')
explore.set_exg_channel_name(2, 'Cz')
explore.set_exg_channel_name(3, 'Fz')
explore.set_exg_channel_name(4, 'Oz')
explore.set_exg_channel_name(5, 'P3')
explore.set_exg_channel_name(6, 'P4')
explore.set_exg_channel_name(7, 'O1')
explore.set_exg_channel_name(8, 'O2')

# Set reference label with all parameters
print("\nSetting reference label...")
explore.set_reference_label('Ref_Node', is_subtracted=True, is_common_average=False)
print("Reference set to 'Ref_Node' (subtracted=True, common_average=False)")

# Test filters
print("\nTesting filters...")

# Add filters one by one
# Bandpass is split into high and low pass filters
# print("Adding bandpass filter: 1-40 Hz")
# explore.stream_processor.add_filter(cutoff_freq=(1, 40), filter_type='bandpass')

print("Adding notch filter: 50 Hz")
explore.stream_processor.add_filter(cutoff_freq=50, filter_type='notch')

# Add a high-pass filter to remove DC offset and very slow drifts
print("Adding high-pass filter: 0.1 Hz")
explore.stream_processor.add_filter(cutoff_freq=0.1, filter_type='highpass')

# Add a low-pass filter to remove high-frequency noise
print("Adding low-pass filter: 100 Hz")
explore.stream_processor.add_filter(cutoff_freq=100, filter_type='lowpass')

print("Configuration complete! Pushing to LSL...")

explore.push2lsl(duration=1000)
