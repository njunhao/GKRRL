#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Reads in analysis_mqte_performance.log from a folder which are subfolders of a folder that is named after the domain.
Folder structure:
    root_folder (given to algorithm as input)
        academic_advising
            experiment_academic_advising_doubleq_epsilon_0001/analysis_mqte_performance.log
            experiment_academic_advising_doubleq_epsilon_0002/analysis_mqte_performance.log
            experiment_academic_advising_doubleq_epsilon_0003/analysis_mqte_performance.log
        recon2
            experiment_recon2_doubleq_epsilon_0001/analysis_mqte_performance.log
            experiment_recon2_doubleq_epsilon_0002/analysis_mqte_performance.log
            experiment_recon2_doubleq_epsilon_0003/analysis_mqte_performance.log

Computes the mean and standard deviation from all logfiles.

Format of logfile is:
    Session #1
    MQTE reduces to a greedy action: 4558
    MQTE reduces greedy actions: 60
    MQTE fail to reduce greedy actions: 160
    Model prediction failed: 18367

@author: alvin
"""

import os
from enum import Enum, auto
import math
import numpy as np
import matplotlib.pyplot as plt
import common_utils

LOGFILE = 'analysis_mqte_performance.log'
CATEGORY_ORDER = ['one_greedy_action', 'lesser_greedy_actions', 'fail_to_reduce', 'fail_to_predict', 'effectiveness_notwithstanding_model', 'effectiveness']


class MSG_TYPE(Enum):
    ONE_GREEDY_ACTION = auto()
    LESSER_GREEDY_ACTIONS = auto()
    FAIL_TO_REDUCE = auto()
    FAIL_TO_PREDICT = auto()
 
MSG_TUPLE = [("MQTE reduces to a greedy action:", MSG_TYPE.ONE_GREEDY_ACTION.value), \
             ("MQTE reduces greedy actions:", MSG_TYPE.LESSER_GREEDY_ACTIONS.value), \
             ("MQTE fail to reduce greedy actions:", MSG_TYPE.FAIL_TO_REDUCE.value), \
             ("Model prediction failed:", MSG_TYPE.FAIL_TO_PREDICT.value)]



"""
Example of logfile:
    Session #1
    MQTE reduces to a greedy action: 4558
    MQTE reduces greedy actions: 60
    MQTE fail to reduce greedy actions: 160
    Model prediction failed: 18367
"""
def parse_results(logfile, verbose = False):
    count = {}
    try:
        if verbose > 1:
            print("Parsing file " + logfile)
        file = open(logfile, "r")
    except IOError:
        if verbose > 0:
            print(logfile + " does not exist")
        return False
    for line in file:
        if not line or line == "\n":
            continue
        msg_type = parse_msg_type(line)
        if msg_type == None:
            continue
        elif msg_type == MSG_TYPE.ONE_GREEDY_ACTION.value:
            count['one_greedy_action'] = int(line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.LESSER_GREEDY_ACTIONS.value:
            count['lesser_greedy_actions'] = int(line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.FAIL_TO_REDUCE.value:
            count['fail_to_reduce'] = int(line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.FAIL_TO_PREDICT.value:
            count['fail_to_predict'] = int(line[line.find(": ")+2:].strip())
    count['effectiveness_notwithstanding_model'] = (count['one_greedy_action']+count['lesser_greedy_actions']) / (count['one_greedy_action']+count['lesser_greedy_actions']+count['fail_to_reduce'])
    count['effectiveness'] = (count['one_greedy_action']+count['lesser_greedy_actions']) / (count['one_greedy_action']+count['lesser_greedy_actions']+count['fail_to_reduce']+count['fail_to_predict'])
    file.close()
    return count


def parse_msg_type(line):
    line = line.lower()
    for phrase, msg_type in MSG_TUPLE:
        phrase = phrase.lower()
        if line.find(phrase) == 0:
            return msg_type
    return None


def get_logfolders(folder):
    logfolders = []
    subfolders = os.listdir(folder)
    for subfolder in subfolders:
        subfolder = common_utils.remove_prefix(subfolder)
        subfolder = os.path.join(folder, subfolder)
        if not os.path.isdir(subfolder):
            continue
        subsubfolders = os.listdir(subfolder)
        subsubfolders = [os.path.join(subfolder, f) for f in subsubfolders]
        subsubfolders = [f for f in subsubfolders if os.path.isdir(f)]
        if subsubfolders:
            logfolders.append(subsubfolders)
    return logfolders


# TODO
def plot(all_agg_count):
    folders = list(all_agg_count.keys())
    domains = [d[d.rfind('/')+1:] for d in folders]
    all_data = []           # len of this = len of CATEGORY_ORDER
    all_data_std_dev = []
    for category in CATEGORY_ORDER:
        data = []           # len of this = num of domains
        data_std_dev = []
        for domain in folders:
            mean_value, std_dev = all_agg_count[domain][category]
            data.append(mean_value)
            data_std_dev.append(std_dev)
        all_data.append(data)
        all_data_std_dev.append(data_std_dev)
    # print(all_data)
    X = np.arange(len(domains))
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X + 0.00, all_data[0], color = 'b', width = 0.25)
    ax.bar(X + 0.25, all_data[1], color = 'g', width = 0.25)
    ax.bar(X + 0.50, all_data[2], color = 'r', width = 0.25)
    ax.bar(X + 0.75, all_data[3], color = 'k', width = 0.25)
    fig.savefig(folders[0]+'/../plot.png')


def run(folder):
    if not folder:
        print('No folder is defined')
        return

    logfolders = get_logfolders(folder)
    if logfolders == []:
        raise Exception('No subfolders found in '+ folder)

    all_agg_count = {}

    for subfolders in logfolders:                       # loop over each domain
        agg_count = {}
        for subfolder in subfolders:                    # loop over each problem of the same domain
            if not os.path.isdir(subfolder):
                continue
            logfile = subfolder+'/'+LOGFILE
            # print("Reading " + logfile + "...")
            verbose = 1
            try:
                count = parse_results(logfile, verbose) # for one problem
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                count = False
            if count:                                    # if successfully analysed results
                for key, value in count.items():
                    if key in agg_count:
                        agg_count[key].append(value)     # each element in the vector pertains to one problem
                    else:
                        agg_count[key] = [value]
            elif verbose == 0:
                print("Failed to analyse " + logfile)
        # print statistics
        base_folder = subfolders[0][:subfolders[0].rfind('/')]
        print('\nAGGREGATION for '+ base_folder)
        all_agg_count[base_folder] = {}
        for key, values in agg_count.items():
            mean_value = sum(values) / len(values)
            sum_difference = 0
            for value in values:
                sum_difference += pow(value-mean_value, 2)
            std_dev = math.sqrt(sum_difference/len(values))
            all_agg_count[base_folder][key] = (mean_value, std_dev)
            print(key + ': mean = ' + str(mean_value) + ', std-dev = ' + str(std_dev))

    # plot figure
    # plot(all_agg_count)


if __name__ == "__main__":
    run('/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/v0-first-order-lfa/MQTE/MQTE-statistics')