    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:10:13 2019

@author: alvin
"""

import os
import subprocess
import batch_plot


group_folders = []                    # each element in group_folders is a list of folders which will be analysed as a group
folders_to_analyse = []
benchmark_folders = {}
module = ''
if 'nalvin' in os.getcwd():
    root_folder = '/home/nalvin/rrl/Results/'
elif '/home/alvin' in os.getcwd():
    root_folder = '/home/alvin/rrl/Results/'
else:
    root_folder = '/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/'

# value can be a list of folders which can be a string or 2-element tuple
# FORMAT: list of strings OR list of 2-element tuple where (string for folder, list of numbers for which subfolder with such number will be analysed)
# Example: ('recon2', [1, 2]) --> then recon2/experiment_recon2_doubleq_epsilon_0001, recon2/experiment_recon2_doubleq_epsilon_0002 will be analysed
benchmark_folders = {
    # 'recon2':                   [(root_folder+'v0-first-order-lfa/MFFS/specific/RC-6/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/specific/RC-6/', list(range(58, 67)))],
    'recon2':                   [(root_folder+'v0-first-order-lfa/MQTE/RC-6/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MQTE/RC-6/', list(range(51, 61)))],
    
    # 'academic_advising':        [(root_folder+'v0-first-order-lfa/MFFS/specific/AA-5/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/specific/AA-5/', list(range(21, 31)))],
    'academic_advising':        [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/AA-5/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/AA-5/', list(range(31, 41)))],
    
    'tiago_fetch':              [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TF-d2/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TF-d2', list(range(131, 141)))],

    'tiago_hri':                [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-1/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-1', list(range(101, 111)))],
    'tiago_hri2':               [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-2/', list(range(11, 21))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-2/', list(range(71, 81)))],
    'tiago_hri3':               [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-2/', list(range(11, 21))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/HRI-2/', list(range(31, 41)))],

    # 'turtlebot_survey':         [(root_folder+'v0-first-order-lfa/MFFS/specific/TS-de4/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/specific/TS-de4/', list(range(71, 81)))],
    'turtlebot_survey':         [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TS-de4/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TS-de4/', list(range(61, 71)))],
    'turtlebot_survey_lfd':     [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TS-de4-lfd/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TS-de4-lfd/', list(range(61, 71)))],
    
    'triangle_tireworld':       [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TT-6/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TT-6/', list(range(31, 41)))],        # goal CX
    # 'triangle_tireworld':       [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TT-6/', list(range(1, 11))), (root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TT-6/', list(range(41, 51)))],        # ground CX    
    'triangle_tireworld_lfd':   [(root_folder+'v0-first-order-lfa/MFFS/adaptive-nil/TT-6-lfd', list(range(1, 11)))],

    'academic_advising_prost':  [root_folder+'v0-first-order-lfa/prost/prost-truth/AA-5'],
    'tiago_hri_prost':          [root_folder+'v0-first-order-lfa/prost/prost-truth/HRI-1'],
    'recon2_prost':             [root_folder+'v0-first-order-lfa/prost/prost-truth/RC-6'],
    'tiago_fetch_prost':        [root_folder+'v0-first-order-lfa/prost/prost-truth/TF-d2'],
    'turtlebot_survey_prost':   [root_folder+'v0-first-order-lfa/prost/prost-truth/TS-de4'],
    'triangle_tireworld_prost': [root_folder+'v0-first-order-lfa/prost/prost-truth/TT-6'],
}
# doesn't work because it produce arguments that are too long for cmd
# all_benchmark = []
# for domain in benchmark_folders:
#     all_benchmark += benchmark_folders[domain]
# benchmark_folders['all'] = all_benchmark


NEW = [
    '/home/nalvin/rrl/Results/v4-uct/TDORMDP-500ep/HRI-2',
    '/home/nalvin/rrl/Results/v4-uct/TDORMDP-500ep/HRI-3',
]


UCT = [
    '/home/nalvin/rrl/Results/v4-uct/UCT-release/HRI-2',
    '/home/nalvin/rrl/Results/v4-uct/UCT-release/RC-6',
    '/home/nalvin/rrl/Results/v4-uct/UCT-release/TF-d2-debug',
    '/home/nalvin/rrl/Results/v4-uct/UCT-release/TS-de4',
    '/home/nalvin/rrl/Results/v4-uct/UCT/HRI-1',
    '/home/nalvin/rrl/Results/v4-uct/UCT/HRI-2',
    '/home/nalvin/rrl/Results/v4-uct/UCT/HRI-3',
    '/home/nalvin/rrl/Results/v4-uct/UCT/RC-6',
    '/home/nalvin/rrl/Results/v4-uct/UCT/TF-d2',
    '/home/nalvin/rrl/Results/v4-uct/UCT/TS-de4',
]


ACE = [
    '/media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/results-2323',
    '/media/alvin/HDD/Academics/PhD/Coding/Experiments/ACE/STACK-TG-STACK',
    '/media/alvin/HDD/Academics/PhD/Coding/Experiments/ACE/STACK-TG-UNSTACK',
]


folders_to_analyse = [ACE]

# folders_to_analyse = [RB + \
#     benchmark_folders['academic_advising'] + \
#     benchmark_folders['tiago_hri'] + \
#     benchmark_folders['tiago_hri'] + \
#     benchmark_folders['recon2'] + \
#     benchmark_folders['turtlebot_survey']]

# this will merge the list of folders into a single list (i.e., they will be plotted on the same fig) if they have the same domain
# folders_to_analyse += batch_plot.merge_folders(specific_criteria+specific_criteria_wrong_epsilon)


# append every entry with their matching benchmark folders
for folder in folders_to_analyse:
    problem = None
    folders = folder
    if isinstance(folder, tuple):
        if folder[0] in benchmark_folders:
            problem = folder[0]
            folders = folder[1]
    if not isinstance(folders, list):
        folders = [folders]
    if problem:
        bfolders = benchmark_folders[problem]
        if not isinstance(bfolders, list):
            bfolders = [bfolders]
        # check all folders are valid
        for folder in bfolders + folders:
            if isinstance(folder, str):
                folder_name = folder 
            elif isinstance(folder[0], str):
                folder_name = folder[0]
            else:
                raise Exception('Unable to determine folder name')
            if not os.path.isdir(folder_name):
                raise Exception('Invalid folder: ' + folder_name)
        folders = bfolders + folders
    group_folders.append(folders)

for folders in group_folders:
    DEBUG = True
    if DEBUG:
        # python doesn't release the memory when doing this
        batch_plot.run(folders, module)
    else:
        cmdline = 'python3 batch_plot.py'
        if isinstance(folders, list) and all([isinstance(folder, str) for folder in folders]):
            # call in a separate process, when it terminates, the OS will release the memory
            # only works if folders is a list of strings
            for folder in folders:
                cmdline += ' ' + folder 
        else:
            logfolders = batch_plot.get_logfolders(folders)
            for folder in logfolders:
                cmdline += ' ' + folder 
        if module != '':
            cmdline += ' ' + module
        res = subprocess.call(cmdline, shell=True)
        if (res != 0):
            print("Unexpected error")