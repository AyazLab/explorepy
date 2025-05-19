

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal

fs = 250

def bp_filter(exg, lf, hf, fs, type='bandpass'):
    N = 3
    b, a = signal.butter(N, [lf / fs, hf / fs], type)
    return signal.filtfilt(b, a, exg)

def notch_filter(exg, fs, f0=50):
    Q = 30.0  # Quality factor
    # Design notch filter
    b, a = signal.iirnotch(f0, Q, fs)
    return signal.filtfilt(b, a, exg)

df_exg = pd.read_csv('exg_data_imp_mode.csv', delimiter=',', dtype=np.float64)

notched = notch_filter(df_exg['ch1'], fs, f0=62.5)
notched = notch_filter(notched, fs, f0=50)
band_passed = bp_filter(notched, 0.5, 30, fs)
plt.plot(df_exg['TimeStamp'], band_passed)
plt.show()
