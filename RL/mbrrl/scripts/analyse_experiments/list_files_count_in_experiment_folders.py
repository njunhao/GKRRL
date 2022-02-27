#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Print number of experiments subfolders in each results folders
Move invalid experiments subfolders to another folder
"""

import sys
import os
import shutil
import subprocess
# import glob
from parser import interpret_name
from parser import parse_mbrrl_results
import common_utils


LOGFILE = 'mbrrl.log'
FULL_LOGFILE = 'mbrrl_console.log'
INVALID_FOLDER = 'invalid'
NUM_LINES_IN_EXCERPT = 200


if os.getcwd().find('/mbrrl/') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl/')+len('/mbrrl/')]
elif os.getcwd().find('/mbrrl') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl')+len('/mbrrl')]
else:
    raise("Unable to determine library path, current directory is " + os.getcwd())


def read_folders(folder, keyphrase = "results-", analyse = False, verbose = False, delete = False, nuke = []):
    results = []
    folder = common_utils.remove_prefix(folder)
    subfolders = sorted(common_utils.get_subfolders(folder, 1, keyphrase))
    for subfolder in subfolders:                # subfolder is the folder for domain
        if not os.path.isdir(subfolder):
            continue
        files_folders = os.listdir(subfolder)   # files_folders is either files or folders for experiments (e.g., experiment_recon2_doubleq_epsilon_0001)
        count = 0
        if any([name_id in subfolder for name_id in nuke]) or '*' in nuke:
            shutil.rmtree(subfolder)
            print('Nuke folder: ' + subfolder)
            continue
        elif verbose:
            print('Folder: ' + subfolder)
        for name_ in files_folders:
            file_path = os.path.join(os.path.abspath(subfolder), name_)
            if not os.path.isdir(file_path):
                if any([name_id in file_path for name_id in nuke]) or '*' in nuke:
                    os.remove(file_path)
                    if verbose:
                        print('    Nuke file: ' + name_)
                elif verbose:
                    print('        >> ' + name_)
                continue                        # is not a folder, skip
            if delete or nuke:
                subsubfolder = os.path.join(subfolder.strip(), name_)
                sub_files_folders = os.listdir(subsubfolder)
                if not sub_files_folders and delete:
                    os.rmdir(subsubfolder)
                    if verbose:
                        print('    Delete empty folder: ' + subsubfolder)
                elif any([name_id in subsubfolder for name_id in nuke]) or '*' in nuke:
                    shutil.rmtree(subsubfolder)
                    if verbose:
                        print('    Nuke folder: ' + subsubfolder)
            elif verbose:
                subsubfolder = os.path.join(subfolder.strip(), name_)
                sub_files_folders = os.listdir(subsubfolder)
                if sub_files_folders:
                    print('    Log Folder: ' + name_)
                    for name__ in sub_files_folders:
                        print('        >> ' + name__)
                else:
                    print('    Empty Log Folder: ' + name_)
            domain, planner, policy = interpret_name( name_[name_.rfind('/')+1:-1] )
            if domain and planner:
                if analyse:
                    try:
                        analysis = parse_mbrrl_results(os.path.join(subfolder.strip(),name_, LOGFILE), False)
                    except Exception as e:
                        analysis = False
                        if hasattr(e, 'message'):
                            print(e.message)
                        else:
                            print(e)
                    if analysis:
                        count += 1
                    else:
                        if delete:
                            shutil.rmtree(os.path.join(subfolder.strip(), name_))
                            print('Delete invalid folder')
                        elif INVALID_FOLDER not in subfolder:                   # do not move invalid folder again
                            logfolder = os.path.join(subfolder.strip(), name_)
                            # move logfolder with invalid logfile to another folder
                            dest = subfolder[: subfolder.rfind('/')] + '-' + INVALID_FOLDER + '/' + subfolder[subfolder.rfind('/')+1 :] + '/' + name_
                            full_logfile_ = logfolder+'/'+FULL_LOGFILE
                            if os.path.isfile(full_logfile_):
                                piped_file = logfolder + '/' + FULL_LOGFILE[:FULL_LOGFILE.rfind('.')] + '-excerpt' + FULL_LOGFILE[FULL_LOGFILE.rfind('.'):]
                                cmdline = 'tail -n' + str(NUM_LINES_IN_EXCERPT) + ' ' + full_logfile_ + ' > ' + piped_file
                                subprocess.call(cmdline, shell=True)
                            shutil.move(logfolder, dest)
                            print('Move invalid folder to: ' + dest)
                else:
                    count += 1

        if count > 0:
            results.append((subfolder, count))
            print(subfolder + ' has ' + str(count) + ' experiments completed')
    return results


if __name__ == "__main__":
    folder = mbrrl_path
    keyphrase = 'results-'                      # set to '' to search in every folder, else it will only search in folders with names that contains this substring
    analyse = False                             # if true, parse logfile and check if it is valid, if not, move logfolder to INVALID_FOLDER
    verbose = False
    delete = False
    nuke = False
    nuke_all = False
    nuke_all_without_asking = False
    nuke_id = []

    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == 'a':
                analyse = True
            elif arg == 'v':
                verbose = True
            elif arg == 'd':
                delete = True                   # this will delete empty folders without asking
            elif arg == 'n':
                nuke = True                     # safety mechanism to prevent accidental nuking, need to give 'n' and IDs to nuke (delete) a folder
            elif arg == 'nuke':
                nuke_all = True
            elif arg == 'NUKE':
                nuke_all_without_asking = True
            elif '/' in arg:
                arg = common_utils.remove_prefix(arg)
                if os.path.isdir(arg):
                    folder = arg
            else:
                try:
                    int(arg)
                    nuke_id.append(arg)          # if giving input 'n', these are IDs to nuke (delete) a folder
                except:
                    pass
    else:
        print('Give optional argument ''a'' to parse logfile for validity, ''v'' for verbose, ''d'' to delete invalid/empty folders, ''n'' to nuke folders with matching IDs')
    if not nuke and nuke_id:
        nuke_id = []
        print('To delete a folder, need to pass in argument ''n'' and the IDs of the folders')
    if nuke_all or nuke_all_without_asking:
        nuke_id = ['*']
        print('Nuking all folders in ' + folder + '!')
        if not nuke_all_without_asking:
            print("Confirm deletion? [y/N]")
            user = input("Confirm deletion? [y/N]")
            if user != 'y' and user != 'Y':
                nuke_id = []
    read_folders(folder, keyphrase, analyse=analyse, verbose=verbose, delete=delete, nuke=nuke_id)