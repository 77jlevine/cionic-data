# %%
# This file will create a stimulation protocol in a .json based on a .csv file you create. This
# .csv file will have the following headers: lhl,lhm,lvl,lrf,lgl,lgm,lta. Below each header,
# you will provide a signal that ranges from 0 to 1. Please save the .csv file that you will be
# uploading into a folder outside of this repository. The .json file will be saved into this same
# folder. You will then copy the contents of the .json file and go to www.cionic.com/a. 
# Navigate to the protocols tab and select New Protocol. Name the protocl and then create. 
# Then you select Text and then delete all text that is there. Then paste the contents of the .json file.
# On the right, select Save as New Version. Now if you update the cionic app, your protocol should be available.

import numpy as np
import pandas as pd
from cionic import triggers
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import json

# %%

# Specify file_path and file_name for the stimulation profiles you created. 
# Please set this up as done in workshop_sample_data/Stimulation Input with 
# the muscle names in the first row (e.g., lhl) and the data below. Please also
# ensure that the data is exactly 101 samples long. The file will not be accepted
# if it is not 101 samples long.

file_path = '' 
file_name = '.csv' # should end with .csv

file_path_stim = file_path + file_name



plot_TF = True

class StimDescription:
    def __init__(self, name,muscle, start_ramp_up,ramp_up, duration, start_ramp_down,ramp_down, intensity, algorithm_up, delay_up, algorithm_down, delay_down):
        self.name = name
        self.muscle = muscle
        self.start_ramp_up = int(start_ramp_up)
        self.ramp_up = int(ramp_up)
        self.duration = int(duration)
        self.ramp_down = int(ramp_down)
        self.intensity = int(intensity)
        self.start_ramp_down = int(start_ramp_down)
        self.algorithm_up = algorithm_up
        self.delay_up = int(delay_up)
        self.algorithm_down = algorithm_down
        self.delay_down = int(delay_down)
        self.default_cycle = 2000
        self.cycle = 1

def StayBtwn0and100(output):
    if output < 0:
        output = output + 100
    elif output > 100:
        output = output - 100
    return int(output)


def FindAlg(start,alg_pcts,alg_names):
    arr = start - np.array(alg_pcts) 
    # Find the index of the minimum value among positive values
    pos = np.where(arr>=0)[0]
    min_positive_index = pos[np.argmin(arr[arr>=0])]
    alg_start = alg_pcts[min_positive_index]
    alg = alg_names[min_positive_index]
    delay = start - alg_start
    return alg, delay


# Need to check this!!!!
muscle_ids = {
    'hl': "custom4",
    'hm': "custom5",
    'vl': "custom7",
    'rf': "custom6",
    'gl': "custom2",
    'gm': "custom3", 
    'ta': "custom1",
    
}

muscle_keys = []
for key,value in muscle_ids.items():
    muscle_keys.append(key)


algorithms = {
    "split": 0,
    "ZeroCrossPMShankX_28": 28,
    "TroughThighX_57": 57,
    "ZeroCrossMPThighX_68": 68,
    "TroughShankX_73": 73,
    "ZeroCrossMPShankX_91": 91
}

alg_names = []
alg_pcts = []
for key,value in algorithms.items():
    alg_names.append(key)
    alg_pcts.append(value)


stim_df = pd.DataFrame()


stim_df = pd.read_csv(file_path_stim)
if not len(stim_df) == 101:
    print('Stimulation protocol could not be created because the file size is incorrect.\nPlease try again with a file that has 101 data points for each muscle and muscles are named correctly.\nSee the Stimulation Input folder within workshop_sample_data for a template.\n')
else: 
    # Cycle through all muscle names and if they are in a list of acceptable muscle_names, then we create the trigger
    col_names = stim_df.columns.tolist()

    if col_names[1][0].lower() == 'r':
        side = 'Right'
    else:
        side = 'Left'

    # Only allow acceptable muscle names
    # muscle_name_set = ['hl','hm','vl','rf','gl','gm','ta']

    # 
    stim_trap = []
    trapezoid_trajectories = []

    fig, axs = plt.subplots(2,4,figsize=(12,8))
    for a in range(len(muscle_keys)):
        matching_cols = [col for col in col_names if col.endswith(muscle_keys[a])]
        if len(matching_cols)==1:
            muscle = muscle_keys[a]

            y_values = np.array(stim_df[matching_cols])[:-1].flatten()
            if np.min(y_values) < 0:
                y_values = y_values - np.min(y_values)
            if np.max(y_values) > 1:
                y_values = y_values/np.max(y_values)

            # Find the Peaks
            peaks1 = find_peaks(y_values)[0]
            peaks2 = find_peaks(np.roll(y_values,50))[0]-50
            for i,pk in enumerate(peaks2):
                peaks2[i] = StayBtwn0and100(pk)
            peaks = np.unique(np.concatenate((peaks1,peaks2)))



        # For each peak
        trapezoids = np.zeros(100)
        for i,pk in enumerate(peaks):
            # Center on the peak
            rollval = 100//2-pk
            tmp = np.roll(y_values,rollval)
            
            k = 50
            while tmp[k] >= tmp[k+1] and tmp[k+1] != 0:
                k+=1
            op_stop = k
            k = 50
            while tmp[k] >= tmp[k-1] and tmp[k-1] != 0:
                k-=1
            op_start = k
                    
            # Find intersect with .95*peak within start and stop range
            pct_plateau = .95
            intersection_95 = np.where(tmp >= pct_plateau * y_values[pk])[0] 
            insct_start = intersection_95[intersection_95>op_start][0]
            insct_stop = intersection_95[intersection_95<op_stop][-1]+1
            
            trap = np.zeros(100)
            trap[op_start:insct_start] = np.linspace(0,pct_plateau*y_values[pk],insct_start-op_start)
            trap[insct_start:insct_stop] = np.ones(insct_stop-insct_start)*pct_plateau*y_values[pk]
            trap[insct_stop:op_stop] = np.linspace(pct_plateau*y_values[pk],0,op_stop-insct_stop)

            trap_roll = np.roll(trap,-rollval)
            trapezoids = trapezoids + trap_roll/.95

            name = muscle + str(i+1)
            custom_muscle = muscle_ids[muscle_keys[a]]

            start_ramp_up = StayBtwn0and100(op_start-rollval)
            ramp_up = insct_start-op_start
            duration =  insct_stop - insct_start
            start_ramp_down = start_ramp_up + ramp_up + duration
            if start_ramp_down>=100:
                start_ramp_down = start_ramp_down-100
            ramp_down = op_stop - insct_stop
            intensity = int(y_values[pk]*100)

            algorithm_up, delay_up = FindAlg(start_ramp_up,alg_pcts,alg_names)
            algorithm_down, delay_down = FindAlg(start_ramp_down,alg_pcts,alg_names)
            stim_trap.append(StimDescription(name,custom_muscle,start_ramp_up,ramp_up, duration, start_ramp_down,ramp_down, intensity, algorithm_up, delay_up, algorithm_down, delay_down))

        if plot_TF:
            axs[int(np.floor(a/4))][a%4].plot(y_values)
            axs[int(np.floor(a/4))][a%4].plot(trapezoids)
            axs[int(np.floor(a/4))][a%4].set_title(muscle_keys[a].upper())
            axs[int(np.floor(a/4))][a%4].set_xlim(0,100)
            axs[int(np.floor(a/4))][a%4].set_ylim(0,1)
        
        trapezoid_trajectories.append(trapezoids)
    plt.tight_layout()
    plt.show()
    # 
    triggers = []
    if side.lower() == 'left':
        side_abr = "l"
        side = "left"
    else:
        side = "right"
        side_abr = "r"

    for trig in stim_trap:
        triggers.append({
            "name": trig.name,
            "muscle": trig.muscle,
            "cycle": trig.cycle,
            "default_cycle": trig.default_cycle,
            "contract": {
                "algo":  trig.algorithm_up,
                "intensityPercent": trig.intensity,
                "delay":  trig.delay_up,
                "ramp":  trig.ramp_up,
                "duration":  trig.duration,
                "context": "\" stim\" RELAY! 0 50 1"
            },
            "relax": {
                "algo":  trig.algorithm_down,
                "delay":  trig.delay_down,
                "ramp":  trig.ramp_down,
                "context": "\" stim\" RELAY! 0 50 1"
            }
            }
        )

    CIONIC_code = {
    "app_xid": "UAUIIdfu3ZoDUb6L-OpfrSNciakTf_d5Bnro3xj3K0s",
    "setup": {
        "program_type": 1,
        "rig": "skeletal",
        "splashImage": "https://app.cionic.com/media/bbce5cde-8ba7-4877-8304-21b99114d87f/gaitassist@3x.png",
        "interfaceSplashImage": "https://app.cionic.com/media/ee1252ab-68a8-4c62-8c39-2661728dc4ce/gaitassist@3x.png",
        "historyIcon": "https://app.cionic.com/media/6f8af303-3237-4c4a-9bae-a8709caccf99/Assist@3x.png",
        "calibration": "imu",
        "keep_awake": "true",
        "reportUrls": [
        {
            "url": "https://raw.githubusercontent.com/cionicwear/cde/develop/analysis/gait.ipynb"
        }
        ],
        "fes": [
        {
            "name": "main",
            "zone": side,
            "split": "split",
            "algorithms": [
            {
                "name": "split",
                "kind": "peak",
                "stream": side_abr + "_shank",
                "component": "x"
            },
            {
                "name": "ZeroCrossPMShankX_28",
                "kind": "cross-",
                "stream": side_abr + "_shank",
                "component": "x",
                "threshold": 0,
                "default_peak": 25,
                "default_trough": -35
            },
            {
                "name": "TroughThighX_57",
                "kind": "trough",
                "stream": side_abr + "_thigh",
                "component": "x",
                "default_peak": 25,
                "default_trough": -35
            },
            {
                "name": "ZeroCrossMPThighX_68",
                "kind": "cross+",
                "stream": side_abr + "_thigh",
                "component": "x",
                "threshold": 0,
                "default_peak": 25,
                "default_trough": -35
            },
            {
                "name": "TroughShankX_73",
                "kind": "trough",
                "stream": side_abr + "_shank",
                "component": "x",
                "default_peak": 25,
                "default_trough": -35
            },
            {
                "name": "ZeroCrossMPShankX_91",
                "kind": "cross+",
                "stream": side_abr + "_shank",
                "component": "x",
                "threshold": 0,
                "default_peak": 25,
                "default_trough": -35
            }
            ],
            "triggers": triggers
        }
        ]
    },
    "phases": [
        {
        "title": "warmup",
        "cmd": "\" stim\" RELAY!",
        "repeat": 1,
        "type": "sequence",
        "segments": [
            {
            "label": "warmup",
            "actions": [
                {
                "instruction": "Press > when ready to begin the protocol",
                "completion": {
                    "type": "man",
                    "count": 1
                }
                }
            ]
            }
        ]
        },
        {
        "title": "no_stim",
        "cmd": "\" stim\" RELAYOFF",
        "repeat": 1,
        "type": "sequence",
        "segments": [
            {
            "label": "no_stim",
            "actions": [
                {
                "instruction": "Warmup at SSV without stim. Press to begin stim",
                "completion": {
                    "type": "man",
                    "count": 1
                }
                }
            ]
            }
        ]
        },
        {
        "title": "stim_active",
        "cmd": "\" stim\" RELAYON",
        "repeat": 1,
        "type": "sequence",
        "segments": [
            {
            "label": "stim_active",
            "actions": [
                {
                "instruction": "Walk with stim. Press to begin cooldown",
                "completion": {
                    "type": "man",
                    "count": 1
                }
                }
            ]
            }
        ]
        },
        {
        "title": "cooldown",
        "cmd": "\" stim\" RELAYOFF",
        "repeat": 1,
        "type": "sequence",
        "segments": [
            {
            "label": "cooldown",
            "actions": [
                {
                "instruction": "cooldown at SSV. Press to finish",
                "completion": {
                    "type": "man",
                    "count": 1
                }
                }
            ]
            }
        ]
        }
    ]
    }

    # Write the dictionary to the file in JSON format
    with open(file_path_stim[:-4] + '.json', "w") as file:
        json.dump(CIONIC_code, file,indent=4)

    print('Saved json file for stimulation to: ' + file_path_stim[:-4] + '.json')