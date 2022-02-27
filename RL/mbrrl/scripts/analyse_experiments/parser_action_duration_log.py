#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Reads in action_duration.log from multiple folders which are subfolders of a root folder.
Computes the mean and standard deviation from all logfiles.

Folder structure:
    root_folder (given to algorithm as input)
        resuls-0001
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0001/action_duration.log 
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0002/action_duration.log 
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0003/action_duration.log 
        resuls-0002
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0001/action_duration.log 
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0002/action_duration.log 
            tiago_hri/experiment_tiago_hri_doubleq_greedy_0003/action_duration.log 

Format of logfile is:
    Action duration [count]:
        find_person(r1, p1) = 19.42 +/- 0 [1]
        find_person(r1, p2) = nil
        find_person(r1, p3) = 17.981 +/- 0 [1]
        give(r1, o1, p1) = nil
        give(r1, o1, p2) = nil
        give(r1, o1, p3) = nil
        give(r1, o2, p1) = nil
        give(r1, o2, p2) = nil

@author: alvin
"""

import os
import math
import common_utils

LOGFILE = 'action_duration.log'


"""
Example of logfile:
    Session #1
    MQTE reduces to a greedy action: 4558
    MQTE reduces greedy actions: 60
    MQTE fail to reduce greedy actions: 160
    Model prediction failed: 18367
"""
def parse_results(logfile, verbose = False):
    data = {}
    try:
        if verbose > 1:
            print("Parsing file " + logfile)
        file = open(logfile, "r")
    except IOError:
        if verbose > 0:
            print(logfile + " does not exist")
        return False
    for line in file:
        if not line or line == "\n" or "=" not in line or "nil" in line:
            continue
        line = line.strip()
        action = line[:line.find("=")].strip()
        duration = float(line[line.find("=")+1 : line.find("+/-")].strip())
        count = int(line[line.find("[")+1 : line.find("]")].strip())
        data[action] = [duration]*count
    file.close()
    return data


def run(folder):
    if not folder:
        print('No folder is defined')
        return

    logfolders = common_utils.get_subfolders(folder)
    if logfolders == []:
        raise Exception('No subfolders found in '+ folder)

    agg_count = {}

    for subfolder in logfolders:                   # loop over each domain
        if not os.path.isdir(subfolder):
            continue
        logfile = subfolder+'/'+LOGFILE
        # print("Reading " + logfile + "...")
        verbose = 0
        try:
            data = parse_results(logfile, verbose) # for one problem
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            data = False
        if data:                                # if successfully analysed results
            for action, durations in data.items():
                if action in agg_count:
                    agg_count[action] += durations
                else:
                    agg_count[action] = durations
        elif verbose == 0:
            print("Failed to analyse " + logfile)
    # print statistics
    print('\nAGGREGATION for '+ folder)
    for action, durations in agg_count.items():
        mean_duration = round(100*sum(durations) / len(durations))/100
        sum_difference = 0
        for duration in durations:
            sum_difference += pow(duration-mean_duration, 2)
        std_dev = round(math.sqrt(sum_difference/len(durations))*100)/100
        print(action + ': mean = ' + str(mean_duration) + ', std-dev = ' + str(std_dev) + ', num samples = ' + str(len(durations)))
        print(durations)


if __name__ == "__main__":
    run('/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/VMWare/ROS/no-uct')