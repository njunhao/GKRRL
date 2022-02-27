#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

This script removes files that matches files_def['delete'] but not files_def['do_not_delete']
"""

import sys
import os
import glob
import shutil
import common_utils


files_def = {
        'do_not_delete': [
            'mbrrl.log',
            'mbrrl_console.log',
            'qvalue_approximation.dat',
            'qvalue_approximation_*.dat',
            'intrinsic_reward.dat',
            'tabu.dat',
            # 'transitions_all.dat', 
            # 'training_data.dat', 
            '*_config.cfg'],

        'delete': [
            # 'mbrrl_console.log', 
            'transitions_all.dat', 
            'data_set.xml', 
            'neural_network.xml', 
            'expression.txt', 
            'training_strategy.xml', 
            'training_strategy_results.dat',
            'analysis_*.log', 
            'lfit_rules_*.dat', 
            'learned_domain.rddl', 
            'learned_domain_*.rddl', 
            'learned_domain_*.ppddl', 
            'transitions_*.dat', 
            'parser_in_*', 
            'parser_out_*', 
            'error_*', 
            'debug_*', 
            'prost_search_*',
            'UCT_search_*',
        ],

        'delete_folders': [
            'fig_'                                  # COMMENT THIS LINE TO DELETE FILES, ELSE DELETE FOLDERS
        ],

        'folder_numbers_to_delete': [               # folder numbers to delete files from (e.g. 0001, 0002, 0003), None to delete from every folder
            # '0002', '0003', '0004'
        ]
}




def main(folder, SAFETY = True):
    subfolders = common_utils.get_subfolders(folder) + [folder]
    if files_def.get('folder_numbers_to_delete', None):
        subfolders = [sb for sb in subfolders if [v for v in files_def['folder_numbers_to_delete'] if v in sb] != []]
    do_not_delete = True
    if not SAFETY:
        print('About to delete some files from the following subfolders...')
        for subfolder in subfolders:
            print('    '+subfolder)
        user = input("Confirm deletion? [y/N]")
        if user != 'y' and user != 'Y':
            print('Deletion aborted!')
            return
        do_not_delete = False
    for subfolder in subfolders:
        if not os.path.isdir(subfolder):
            continue                                        # will not be a directory if deleted
        for folder_pattern in files_def.get('delete_folders', None):
            if folder_pattern in subfolder:
                print('About to delete subfolder...' + subfolder)
                user = input("Confirm deletion? [y/N]")
                if user != 'y' and user != 'Y':
                    print('Deletion aborted!')
                    break
                else:
                    shutil.rmtree(subfolder)
                break
        if files_def.get('delete_folders', None) and files_def['delete_folders']:
            continue                                        # do not delete any files if deleting folders
        files_to_delete = []
        for file_pattern in files_def['delete']:
            matched_files = glob.glob(subfolder+'/'+file_pattern)
            if matched_files:
                files_to_delete = files_to_delete+matched_files
        for file_pattern in files_def['do_not_delete']:
            matched_files = glob.glob(subfolder+'/'+file_pattern)
            for mf in matched_files:
                files_to_delete = [x for x in files_to_delete if x != mf]
        if files_to_delete:
            if SAFETY:
                do_not_delete = True
                print('The following files will be deleted...')
                for f in files_to_delete:
                    print('    '+f)
                user = input("Delete the above files? [y/N]")
                if user == 'y' or user == 'Y':
                    user = input("Are you sure? [y/N]")
                    if user == 'y' or user == 'Y':
                        do_not_delete = False
            if not do_not_delete:
                common_utils.remove_files(files_to_delete, verbose = False)
            else:
                print('Deletion aborted!')


if __name__ == "__main__":
    SAFETY = True                   # if True, user need to enter yes to delete files in each subfolder, otherwise, just a single confirmation for all subfolders will do
    folder = None
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == 'nuke':
                SAFETY = False
            elif '/' in arg:
                arg = common_utils.remove_prefix(arg)
                if os.path.isdir(arg):
                    folder = arg
    if folder is None:
        print('Usage: python3 remove_optional_files.py [FOLDER] <nuke>')
    else:
        main(folder, SAFETY)