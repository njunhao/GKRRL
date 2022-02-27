#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Copies all files as declared in filenames from a folder, searches through its subfolders till the end, and preserves the folder structures (copies the folders as well)
"""

import sys
import os
import glob
import shutil
import common_utils

filenames = ['action_duration.log']
# filenames = ['mbrrl.log', 'mbrrl_console.log']
# filenames = ['mbrrl.log', 'qvalue_approximation.dat', 'qvalue_approximation_dual.dat', 'qvalue_approximation_intrinsic.dat', 'qvalue_approximation_dual_intrinsic.dat', 'intrinsic_reward.dat', 'tabu.dat']
# filenames = ['*.png']
multiple_num = None            # if not None, then only folders with numbers which is divisible by multiple_num will be copied


def main(folder, dest_folder):
    folder = common_utils.remove_prefix(folder)
    dest_folder = common_utils.remove_prefix(dest_folder)
    subfolders = common_utils.get_subfolders(folder)
    print('Found ' + str(len(subfolders)) + ' subfolders')
    for subfolder in subfolders:
        if multiple_num is not None:
            try:
                index = int(subfolder[-4:])
                if index % multiple_num != 0:
                    continue 
            except:
                pass
        for filename in filenames:
            files_to_copy = common_utils.get_files_from_folder(subfolder, filename)
            if files_to_copy:
                print('Copy ' + str(len(files_to_copy)) + ' files')
                common_utils.copy_files_with_folders(files_to_copy, folder, dest_folder)



if __name__ == "__main__":
    folder = ''
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if '/' in arg:
                arg = common_utils.remove_prefix(arg)
                if os.path.isdir(arg):
                    folder = arg
                    break
    if folder == '':
        raise Exception('Give one argument for folder location')
    dest_folder = folder +'-COPY'
    main(folder, dest_folder)
    print('Copied to ' + dest_folder)