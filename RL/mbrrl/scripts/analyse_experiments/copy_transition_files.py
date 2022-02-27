#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Copies all files as declared in filenames from a folder, searches through its subfolders till the end, and copies the files to dest_folder
Since there may be conflicts in filenames, append '_x' where x is a num to filenames to avoid conflicts
"""

import sys
import os
import glob
import shutil
import common_utils

filenames = ['transitions_all.dat']


def main(folder, dest_folder):
    subfolders = common_utils.get_subfolders(folder)
    print('Found ' + str(len(subfolders)) + ' subfolders')
    os.makedirs(os.path.dirname(dest_folder), exist_ok=True)
    for subfolder in subfolders:
        for filename in filenames:
            files_to_copy = common_utils.get_files_from_folder(subfolder, filename)
            if files_to_copy:
                print('Copy ' + str(len(files_to_copy)) + ' files')
                common_utils.copy_files_to_a_folder(files_to_copy, dest_folder)



if __name__ == "__main__":
    folder = ''
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    elif folder == '':
        print('Usage: python3 copy_transition_files.py [folder]')
    if folder != '':
        folder = common_utils.remove_prefix(folder)
        dest_folder = folder
        main(folder, dest_folder)