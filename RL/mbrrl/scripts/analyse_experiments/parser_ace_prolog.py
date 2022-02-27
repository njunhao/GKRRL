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
import math
import common_utils

LOGFILE = 'blocks.results'


# Example Logfile
# 0   0.0   30.0 
# 10   0.0   30.0 
# 20   0.0   30.0 
# 30   0.0   30.0 
# 40   0.0   30.0 
# 50   0.0   30.0 
# 60   0.0   30.0 
# 70   0.0   30.0 
# 80   0.0   30.0 
# 90   0.0   30.0 
# 100   0.0   30.0 
# # This test took 1.76 CPU seconds
def parse_results(logfile, verbose = False):
    results = []
    runtime = None
    try:
        if verbose > 1:
            print("Parsing file " + logfile)
        file = open(logfile, "r")
    except IOError:
        if verbose > 0:
            print(logfile + " does not exist")
        return False
    for line in file:
        if '#' in line:
            runtime = float(line[line.find('took')+4:line.find('CPU')].strip())
        else:
            values = tuple([float(v.strip()) for v in line.split(' ') if v.strip() != ''])          # (episode, reward, num of actions)
            if values[0] > 0:                                                                       # ignore episode 0
                results.append(values)
            # episode = substrings[0]
            # reward substrings[1]
            # num_actions = substrings[2]
    file.close()
    return (results, runtime)


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
        if subsubfolders == []:
            logfolders.append(subfolder)
        else:
            logfolders.append(subsubfolders)
    if logfolders:
        return logfolders
    else:
        return [folder]


def list_addition(list1, list2):
    zipped = zip(list1, list2)
    result = []
    for v1, v2 in zipped:
        result.append(v1+v2)
    return result


def list_substraction(list1, list2):
    zipped = zip(list1, list2)
    result = []
    for v1, v2 in zipped:
        result.append(v1-v2)
    return result


def plot(episodes, mean_rewards, std_devs):
    subplot_x = 0
    subplot_y = 0
    fig, ax = plt.subplots(2, 2)
    # plt.setp(ax, ylim=[0.0, 1.0], yticks=[0.0, 0.5, 1.0], xticks=[2, 4, 6, 8, 10])
    ax[subplot_x][subplot_y].title.set_text('Title')
    ax[subplot_x][subplot_y].plot(episodes, mean_rewards, linewidth=2, label='Legend')
    ax[subplot_x][subplot_y].fill_between(episodes, list_substraction(mean_rewards, std_devs), list_addition(mean_rewards, std_devs), alpha=0.2)
    fig.tight_layout()
    #plt.xticks(range(1, num_data+1, 1))
    plt.legend(ncol=3, loc='upper center', bbox_to_anchor=(-0.1, -0.3), framealpha=0.0)
    plt.savefig('result.png', format='png', bbox_inches="tight", dpi=300)


def run(folder):
    if not folder:
        print('No folder is defined')
        return

    logfolders = get_logfolders(folder)
    if logfolders == []:
        raise Exception('No subfolders found in '+ folder)
    all_results = []
    for subfolders in logfolders:
        if not isinstance(subfolders, list):
            subfolders = [subfolders]
        for subfolder in subfolders:                    # loop over each problem of the same goal
            if not os.path.isdir(subfolder):
                continue
            print(subfolder)
            logfile = subfolder+'/'+LOGFILE
            print("Reading " + logfile + "...")
            verbose = 1
            results = []
            try:
                results, runtime = parse_results(logfile, verbose)  # for one problem
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                results = None
                # runtime = None
            if results:
                all_results.append(results)
            elif verbose == 0:
                print("Failed to analyse " + logfile)

        if all_results:
            num_data_points = len(all_results[0])
            num_results = len(all_results)
            sum_rewards = []
            for i in range(num_data_points):
                sum_reward = 0
                for values in all_results:
                    sum_reward += values[i][1]
                sum_rewards.append(sum_reward)
            mean_rewards = [r/num_results for r in sum_rewards]
            std_devs = []
            for i in range(num_data_points):
                sum_difference = 0
                for values in all_results:
                    sum_difference += pow(values[i][1]-mean_rewards[i], 2)
                std_devs.append(math.sqrt(sum_difference/num_results))
            # plot figure
            plot([v[0] for v in all_results[0]], mean_rewards, std_devs)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # run('/media/alvin/HDD/Academics/PhD/Coding/StatisticalLearner/ACE-ilProlog-1.2.20/RRL-benchmark/STACK-TG')
    run('/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/ACE')

