# %%
import numpy as np
import pandas as pd
from cionic import tools, triggers
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
import tkinter as tk
from tkinter import filedialog
import json

# %%
# Select file

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open the file dialog
file_path_emg = filedialog.askopenfilename(
    title="Select a .npz file",
    filetypes=[("NumPy compressed", "*.npz"), ("All files", "*.*")]
)


npz = np.load(file_path_emg)
segments = pd.DataFrame(npz['segments'])
stream_names = np.unique(segments['position'])

# 
if ('l_shank_emg' in stream_names or 'l_emg' in stream_names) and ('r_shank_emg' in stream_names or 'r_emg' in stream_names):
    side = 'both'
elif 'l_shank_emg' in stream_names or 'l_emg' in stream_names:
    side = 'left'
elif 'r_shank_emg' in stream_names or 'r_emg' in stream_names:
    side = 'right'

streams_quat = tools.load_streams(npz, convert=True, stream='fquat')
imu_out = []
for i in [1, 0]:
    imu_out.append(pd.DataFrame(streams_quat[i]['values']))

print('filter stream == emg')
streams = [ x for x in set(npz['segments']['stream']) if 
    not x.startswith('shtp_') # shtp_ streams should be redundant
    and x not in ['frsp', 'regs', 'charge']   # register streams
    ]
data_dict, times, components = tools.stream_data(npz, streams=streams, degrees=True)
regs_dict = tools.stream_regs(npz)
stream_EMG = []
for item in components:
    if 'emg' in item and 'adcf' not in item:
        stream_EMG.append(item)
emg_elapsed_s = np.array(pd.DataFrame(npz[stream_EMG[1].split()[0] + '_emg'])['elapsed_s'])
emg_fs = 1995

fil = {
    'filter' : None,
}

fft = 'db'
a1_scale = 1
a2_scale = 10000
signals, legends = tools.compute_signals(data_dict, regs_dict, stream_EMG, times, fil, 100, 'db', [a1_scale,a2_scale])
# signals['sig'] contains 8 structures of ['stream'] and ['elapsed_s']. Stream is the data, elapsed_s is the time

chanpos_string = segments.loc[segments[segments['stream']=='emg']['chanpos'].index[0], "chanpos"]

# Split the string into individual values
muscle_names = chanpos_string.split()

df_emg = pd.DataFrame()
df_emg['Time'] = signals['sig'][0]['elapsed_s']
if side.lower() == 'right':
    reord = [7,5,0,1,4,6,2]
else:
    reord = [0,1,7,5,3,2,6]
for od in reord:
    df_emg[muscle_names[od]] = signals['sig'][od]['stream']


# 1. Extract source (IMU) time and signal
imu_time = imu_out[0]['elapsed_s']   # e.g., shape (N_imu,)
imu_signal = imu_out[0]['x']         # shape (N_imu,)

# 2. Extract target (EMG) time
emg_time = signals['sig'][0]['elapsed_s']     # shape (N_emg,)

# 3. Interpolation function
interp_func = interp1d(imu_time, imu_signal, kind='linear', bounds_error=False, fill_value="extrapolate")

# 4. Evaluate at EMG timestamps
upsampled_imu = interp_func(emg_time)
df_emg['ShankSagittal'] = upsampled_imu
df_emg.to_csv(file_path_emg[:-4]+'_emg.csv')

print('File written to ' + file_path_emg[:-4]+'_emg.csv')
