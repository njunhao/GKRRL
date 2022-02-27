#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

This script monitors disk usage and RAM usage, and kills all experiments if exceeds threshold
"""

import os
import subprocess
import time
from datetime import datetime
from datetime import date
import sys
sys.path.insert(0, os.getcwd()+"/../analyse_experiments")
# from analyse_experiments.list_files_count_in_experiment_folders import read_folders
import list_files_count_in_experiment_folders as lsof


# parameters to set
PORT_NUM = 2424
SETTING_FILE = 'ros'
LOGFILE = 'mbrrl_console.log'
NUM_EXPERIMENTS = 10                  # number of experiments to run
CHECK_FREQUENCY = 60                  # check usage in every CHECK_FREQUENCY seconds
MAX_MONITORING_TIME = 30*60*60*24     # run this script for this duration in seconds
MAX_STUCK_DURATION = 600              # if file size is the same for this duration in seconds, restart experiments
PHRASE = "Error: couldn't connect to server on port"

if os.getcwd().find('/mbrrl/') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl/')+len('/mbrrl/')]
elif os.getcwd().find('/mbrrl') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl')+len('/mbrrl')]
else:
    raise("Unable to determine library path, current directory is " + os.getcwd())
FILEPATH = mbrrl_path+'/results-' + str(PORT_NUM) + '/current/' + LOGFILE


def get_command(mode, num_of_experiments_done = 0):
    if num_of_experiments_done < 10:
        bash_cmd = 'bash ' + mbrrl_path + 'scripts/run_experiments/run-ros-experiments.sh ' + \
                    mode + ' ' + SETTING_FILE + ' ' + str(PORT_NUM)
        if num_of_experiments_done > 0:
            bash_cmd += ' ' + str(num_of_experiments_done)
    else:
        bash_cmd = 'bash ' + mbrrl_path + 'scripts/run_experiments/run-ros-experiments.sh ' + \
                    'kill ' + SETTING_FILE + ' ' + str(PORT_NUM)
    return bash_cmd




if __name__ == "__main__":
    t0 = time.time()
    if os.path.isfile(FILEPATH):
        file_size = os.path.getsize(FILEPATH)
    else:
        file_size = 0
    prev_file_size = file_size
    count = 0
    print('Running '+str(NUM_EXPERIMENTS) + ' experiments')
    print('Please set up the tmux session for ROS manually, this python script will not set up the ROS environment correctly')
    new_run = True

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_lapsed = round(time.time() - t0)
        if os.path.isfile(FILEPATH):
            file_size = os.path.getsize(FILEPATH)
        else:
            file_size = 0
        print('Current Time =', date.today(), current_time, ', File Size =', file_size, 'bytes, monitoring for ', time_lapsed, 'seconds')
        if prev_file_size == file_size:
            count += 1
        else:
            prev_file_size = file_size
            count = 0
        results = lsof.read_folders(mbrrl_path, "results-2424", True)
        if results:
            num_of_experiments_done = results[0][1]
        else:
            num_of_experiments_done = 0
        if new_run or (count-1)*CHECK_FREQUENCY >= MAX_STUCK_DURATION or num_of_experiments_done >= NUM_EXPERIMENTS:
            new_run = False
            if num_of_experiments_done == 0: # or file_size == 0
                mode = 'run'
                print('Run experiment')
            elif num_of_experiments_done < NUM_EXPERIMENTS:
                mode = 'rerun'
                print('Continue experiment with ' + str(num_of_experiments_done) + ' done previously')
            else:
                mode = 'kill'
                print('Kill experiment')
            res = subprocess.call(get_command(mode, num_of_experiments_done), shell=True)
            if mode == 'kill':
                print('Completed monitoring... Current Time =', date.today(), current_time, ', File Size =', file_size, 'bytes, monitoring for ', time_lapsed, 'seconds')
                break
            count = 0
            file_size = 1
            prev_file_size = 0
        elif time_lapsed > MAX_MONITORING_TIME:
            print('End monitoring... Current Time =', date.today(), current_time, ', File Size =', file_size, 'bytes, monitoring for ', time_lapsed, 'seconds')
            break
        time.sleep(CHECK_FREQUENCY)