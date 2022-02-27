#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Rename all experiment folders in a main folder by changing the starting number
Each experiment folder is named such that the number is appended at the back (e.g. _0001, _0002)
Then cut and paste all the files into the same folder
"""

import sys
import os
import shutil
import common_utils
import rename_experiment_folders as REF

invalid_domain_name = ['current']
# special_characters = "!@#$%^&*()+?=,<>"
special_characters = "!@#$%^&*()+?=,<>/"

# textfile contains folders separated by newline to indicate grouping of folders, can be output of list_files_count_in_experiment_folders.py
# Example (manually add newline to break apart groups):
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2311/grid_survey has 4 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2312/grid_survey has 10 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2314/grid_survey has 11 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2315/grid_survey has 6 experiments completed
#
# optional_folder_name
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2331/academic_advising has 8 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2332/academic_advising has 4 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2333/academic_advising has 10 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2334/academic_advising has 3 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2335/academic_advising has 10 experiments completed
# /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2336/academic_advising has 10 experiments completed
def parse_file(filename):
    filename = common_utils.remove_prefix(filename)
    try:
        print("Parsing file '" + filename + "'")
        file = open(filename, "r")
    except IOError:
        print(filename + " does not exist")
        return [], []
    sets_of_folders_to_merge = []
    set_of_folders_to_merge = []
    folder_names = []
    folder_name = ''

    for line in file:
        if line != "\n" and line:
            line = line.strip()
            remove_domain_name = False
            if ' ' in line:                                                # quick hack: assume if line has spacing, then it is the output from list_files_count_in_experiment_folders.py
                line = line[: line.find(' ')]
                remove_domain_name = True
            line = common_utils.remove_prefix(line)
            if os.path.isdir(line):                                        # this checks if line is an existing directory, if we want to create a new directory, this needs to be modified
                if remove_domain_name:
                    line = line[: line.rfind('/')]                         # quick hack: /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2331/academic_advising --> /home/nalvin/rrl/run_mbrrl/RL/mbrrl/results-2331/
                set_of_folders_to_merge.append(line)
            elif not any(c in special_characters for c in line):           # cannot have special characters in folder name
                folder_name = line
            else:
                print('Unrecognised line: ' + line)
        elif set_of_folders_to_merge:
            sets_of_folders_to_merge.append(set_of_folders_to_merge)
            set_of_folders_to_merge = []
            folder_names.append(folder_name)
            folder_name = ''
    if set_of_folders_to_merge:
        sets_of_folders_to_merge.append(set_of_folders_to_merge)
        folder_names.append(folder_name)
    print("Finished parsing file")
    return sets_of_folders_to_merge, folder_names


def merge(folders, dest_folder_name = None, sort_by_domain = True, verbose = True, debug = False):
    folders = common_utils.remove_prefix(folders)
    files_to_copy = []

    possible_domains = []
    for folder in folders:
        if os.path.isdir(folder):
            contents = os.listdir(folder)
            subfolders = []
            for content in contents:
                content_path = os.path.join(folder, content)
                if os.path.isdir(content_path):
                    subfolders.append(content)
                elif os.path.isfile(content_path) and content_path not in files_to_copy:
                    files_to_copy.append(content_path)
            if subfolders:
                possible_domains += [sb for sb in subfolders if sb not in possible_domains and sb not in invalid_domain_name]

    move_to_user_defined_folder = False
    if not sort_by_domain:
        possible_domains = ['']
    for domain in possible_domains:
        if sort_by_domain: 
            domain_folders = [f+'/'+domain for f in folders]
        else:
            domain_folders = folders
        dest_folder = domain_folders[0]
        if dest_folder_name and not any(c in special_characters for c in dest_folder_name):
            move_to_user_defined_folder = True
            indices = [i for i, c in enumerate(dest_folder) if c=='/']
            dest_folder = dest_folder[:indices[-2]] + '/' + dest_folder_name + '/' + dest_folder[indices[-1]:]

        starting_nums = {}
        for folder in domain_folders:
            if not os.path.isdir(folder):
                continue
            keyed_logfolders = REF.get_folder_structure(folder)
            if keyed_logfolders:
                if domain_folders:
                    print('Merging for domain: ' + domain + ' into folder: ' + dest_folder)
                for key_, logfolders in keyed_logfolders.items():
                    REF.rename(folder, starting_nums.get(key_, 1), key_)
                    # accumulate number of folders (sorted by their keys) to compute the starting number for renaming folders
                    if key_ not in starting_nums.keys():
                        starting_nums[key_] = len(logfolders)+1
                    else:
                        starting_nums[key_] += len(logfolders)
                for subfolder in [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]:
                    if debug:
                        print('Moving from ' + os.path.join(folder, subfolder) + ' to ' + os.path.join(dest_folder, subfolder))
                    else:
                        if verbose:
                            print('Moving from ' + os.path.join(folder, subfolder) + ' to ' + os.path.join(dest_folder, subfolder))
                        shutil.move(os.path.join(folder, subfolder), os.path.join(dest_folder, subfolder))
    # copy files (experiment setting, etc.)
    dest_folder = dest_folder+'/../'
    if move_to_user_defined_folder and os.path.isdir(dest_folder):
        for file in files_to_copy:
            if debug:
                print('Moving from ' + file + ' to ' + dest_folder)
            else:
                if verbose:
                    print('Moving from ' + file + ' to ' + dest_folder)
                shutil.copy2(file, dest_folder)


if __name__ == "__main__":
    folders = []
    # folders.append('/media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/results-2424')
    filename = ''
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    elif not folders:
        print('Usage: python3 merge_experiment_folders.py [filename]')

    # get groups of folders which are to be merged into a single folder by reading from a text file
    sets_of_folders_to_merge, folder_names = parse_file(filename)
    if sets_of_folders_to_merge:
        can_merge = True
        print("Checking number of files to merge")
        for set_of_folders_to_merge in sets_of_folders_to_merge:
            if len(set_of_folders_to_merge) > 10:
                user = input('More than 10 folders are being merged into one, are you sure? [y/N]')
                if user == 'n' or user == 'N':
                    can_merge = False
                    break
        if can_merge:
            count = 0
            for set_of_folders_to_merge, folder_name in zip(sets_of_folders_to_merge, folder_names):
                count += 1
                print("Merging set #" + str(count) + "/" + str(len(sets_of_folders_to_merge)))
                # if folder_name is given, copy all files from set_of_folders_to_merge to folder_name, else, copy them to the first folder in set_of_folders_to_merge
                merge(folders = set_of_folders_to_merge, dest_folder_name = folder_name, sort_by_domain = True, verbose = True, debug = False)
            print('Destination folders are:')
            for set_of_folders_to_merge, folder_name in zip(sets_of_folders_to_merge, folder_names):
                if folder_name:
                    print('     ' + folder_name)
                else:
                    print('     ' + set_of_folders_to_merge[0])
    elif folders:
        merge(folders)