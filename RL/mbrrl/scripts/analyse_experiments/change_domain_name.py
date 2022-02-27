#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

For all files of interest as declared in FILENAMES from a folder, searches through its subfolders till the end, and replace OLD_DOMAIN_NAME with NEW_DOMAIN_NAME
in file contents as well as filenames and folder names
"""

import os
# import glob
import shutil
import common_utils
import subprocess


# forget about mbrrl_console.log, if timeout, this creates an error file which is a copy of it
# when the program terminates, it tries to delete the file but since we rename the folder, this cannot be done
FILENAMES = ['mbrrl.log', '*_config.cfg'] # 'mbrrl_console.log'
OLD_DOMAIN_NAME = 'simple_survey'
NEW_DOMAIN_NAME = 'grid_survey'
TIMEOUT_SECONDS = 10         # for mbrrl_console.log, this will timeout as the log is long but we only need to replace the first few lines which shouldn't take so long



# perform grep replace string command with timeout
def replace_string(filename):
    cmdline = 'grep -rl \'' + OLD_DOMAIN_NAME + '\' ' + filename + ' | xargs sed -i \'s,' + OLD_DOMAIN_NAME + ',' + NEW_DOMAIN_NAME + ',g\' ' + filename
    try:
        res = subprocess.call(cmdline, shell=True, timeout=TIMEOUT_SECONDS)     # if timeout, then this will return Exception
    except:
        pass



def main(folder):
    folder = common_utils.remove_prefix(folder)
    subfolders = common_utils.get_subfolders(folder)
    print('Found ' + str(len(subfolders)) + ' subfolders')
    filenames = [filename.replace('*', OLD_DOMAIN_NAME) for filename in FILENAMES]      # replace wildcard with OLD_DOMAIN_NAME
    
    # for each subfolder, find the files which match FILENAMES, then replace the contents in it
    for subfolder in subfolders:
        for filename in filenames:
            files_to_copy = common_utils.get_files_from_folder(subfolder, filename)
            if files_to_copy:
                for file in files_to_copy:
                    # replace contents of file
                    replace_string(file)
                    # rename files
                    filename = file[file.rfind('/')+1 :]
                    if OLD_DOMAIN_NAME in filename:
                        print('Renaming file ' + file)
                        filename = filename.replace(OLD_DOMAIN_NAME, NEW_DOMAIN_NAME)
                        new_file = file[: file.rfind('/')+1] + filename
                        os.rename(file, new_file)
    # change all the folder names after modifying / renaming the files, else will have error
    subfolders.reverse()                    # need to reverse to begin renaming subfolders before folder
    for subfolder in subfolders:
        folder_name = subfolder[subfolder.rfind('/')+1 :]
        if OLD_DOMAIN_NAME in folder_name:
            folder_name = folder_name.replace(OLD_DOMAIN_NAME, NEW_DOMAIN_NAME)
            new_folder_name = subfolder[: subfolder.rfind('/')+1] + folder_name
            os.rename(subfolder, new_folder_name)
            print('Renaming folder ' + subfolder)


if __name__ == "__main__":
    folders = [
        '/media/alvin/HDD/New/v2-KR-DEPTH-MQE-DELETE-COPY'

        ]
    for folder in folders:
        main(folder)