#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Rename all experiment folders in a main folder by changing the starting number
Each experiment folder is named such that the number is appended at the back (e.g. _0001, _0002)
"""

import os
import sys
from operator import itemgetter
import common_utils
from parser import interpret_name as interpret_name


def get_folder_structure(root_folder):
    if not os.path.isdir(root_folder):
        print('Unable to get structure of a non-folder: ' + root_folder)
        return []
    subfolders = os.listdir(root_folder)
    logfolders = {}
    for folder in subfolders:
        if not os.path.isdir(os.path.join(root_folder, folder)):
            continue
        try:
            # separate the folders into their instance, planner, policy as these are to be numbered separately
            instance, planner, policy = interpret_name(folder)
            key = instance
            if planner:
                key += '-' + planner 
            if policy:
                key += '-' + policy
            if key in logfolders.keys():
                logfolders[key] += [(folder, int(folder[-4:]))]
            else:
                logfolders[key] = [(folder, int(folder[-4:]))]
        except:
            print(folder + ' is an invalid experiment folder')
            continue
    return logfolders


def rename(root_folder, starting_num, selected_key = None):
    logfolders = get_folder_structure(root_folder)
    for key_, folders in logfolders.items():
        if selected_key is not None and selected_key != key_:
            continue
        folders.sort(key=itemgetter(-1), reverse = True)    # sort the list in ascending order of their num in the folder name
        starting_num_ = starting_num
        # rename to temporary names first to avoid trying to rename a folder to a name that already exist
        for folder in folders:
            os.rename(root_folder+'/'+folder[0], root_folder+'/'+folder[0]+'_')
        for folder in folders:
            num_str = "%04d" % (starting_num_+len(folders)-1)  
            print('Rename ' + folder[0] + ' to ' + folder[0][:-4]+num_str)
            os.rename(root_folder+'/'+folder[0]+'_', root_folder+'/'+folder[0][:-4]+num_str)
            starting_num_ -= 1



if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception('./rename_folders.py [str: folder name] [int: starting num]')
    path = sys.argv[1]
    rename(common_utils.remove_prefix(path), int(sys.argv[2]))