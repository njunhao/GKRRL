#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin
"""

import os
import glob
import shutil

prefix = ['sftp://alvin@137.195.63.205', 'sftp://robotarium.hw.ac.uk', 'sftp://137.195.63.205']



def list2string(lsof_strings, sort = True, linebreak = False, delimiter = ' '):
    if lsof_strings is None or lsof_strings == "":
        return ""
    elif len(lsof_strings) == 1:
        return lsof_strings[0]
    elif isinstance(lsof_strings, str):
        return lsof_strings
    s = ""
    if sort:
        lsof_strings.sort()
    for value in lsof_strings:  # sort by alphabetical order
        if isinstance(value, list):
            value = value[0]
            if linebreak: 
                s += "\n"
                linebreak = False
        elif isinstance(value, str):
            s += value 
            if linebreak: 
                s += "\n"
                linebreak = False
            else:
                s += delimiter
    return s[:-1]


def remove_prefix(values):
    if isinstance(values, list):
        for pf in prefix:
          values = [value.replace(pf, '') for value in values]
    else:
        for pf in prefix:
          values = values.replace(pf, '')
    return values


def remove_files(files, path = '', verbose = True):
    if not isinstance(files, list):
        files = [files]
    files = list(set(files))                    # remove duplicates
    for file in files:
        try:
            os.remove(path + '/' + file)
        except:
            if verbose:
                print("Warning: Couldn't remove " + file)


# copies files from src_folder to dest_folder while perserving the folder structure
# Example:
# A/B/C/file.txt with src_folder = 'A' and dest_folder = 'D' will be copied to 'D/B/C/file.txt'
def copy_files_with_folders(files, src_folder, dest_folder, verbose = True):
    if not isinstance(files, list):
        files = [files]
    for file in files:
        try:
            # get subpath of file leading from src_folder to the folder file is in, then append this subpath to dest_path
            dest_path = dest_folder + '/' + file[file.find(src_folder)+len(src_folder) :]
            # get path to folder which file will be copied to
            dest_folder_ = dest_path[: dest_path.rfind('/')] + '/'
            # create folder
            os.makedirs(os.path.dirname(dest_folder_), exist_ok=True)
            # copy file
            shutil.copy2(file, dest_path)
        except:
            if verbose:
                print("Warning: Couldn't copy " + file + " to " + dest_path)


# copies files to dest_folder where files might be from different folders but have the same name
# Since the same filename cannot exist in a folder, a different filename must be used
# Example:
# A/B/C/file.txt and D/E/F/file.txt with dest_folder = 'Z' will be copied to 'Z/file_1.txt' and 'Z/file_2.txt'
def copy_files_to_a_folder(files, dest_folder, verbose = True):
    MAX_COUNTER = 100
    if not isinstance(files, list):
        files = [files]
    for file in files:
        try:
            # get filename
            filename = file[file.rfind('/') :]
            counter = 0
            while counter == 0 or os.path.isfile(dest_path):
                counter += 1
                if counter > MAX_COUNTER:
                    raise Exception("Couldn't copy " + file)
                # append a '_x" where x is a num to filename
                dest_filename = filename[: filename.rfind('.')] + '_' + str(counter) + filename[filename.rfind('.') :]
                # file path to copy to
                dest_path = dest_folder + '/' + dest_filename
            shutil.copy2(file, dest_path)
        except:
            if verbose:
                print("Warning: Couldn't copy " + file + " to " + dest_path)


# return file path of files in subfolders of folder if the file has name = filename
# if filename contains wildcard '*', then a file matching will be done
def get_files_from_folder(folder, filename = '*', check_subfolders = False):
    files = []
    if check_subfolders:
        subfolders = os.listdir(folder)
        for subfolder in subfolders:
            subfolder = folder+'/'+subfolder
            if os.path.isdir(subfolder):
                if '*' in filename:
                    matching_filenames = glob.glob(os.path.join(folder, subfolder, filename))
                    for matching_filename in matching_filenames:
                        if os.path.isfile( os.path.join(folder, subfolder, matching_filename) ):
                            files.append(os.path.join(folder, subfolder, matching_filename))
                elif os.path.isfile( os.path.join(folder, subfolder, filename) ):
                    files.append(os.path.join(folder, subfolder, filename))
            elif os.path.isfile(subfolder) and subfolder[subfolder.rfind('/')+1 :] == filename:
                files.append(subfolder)
    else:
        if '*' in filename:
            matching_filenames = glob.glob(os.path.join(folder, filename))
            for matching_filename in matching_filenames:
                if os.path.isfile( os.path.join(folder, matching_filename) ):
                    files.append(os.path.join(folder, matching_filename))
        elif os.path.isfile( os.path.join(folder, filename) ):
            files.append(os.path.join(folder, filename))
    return files



def get_subfolders(folder, nested = None, keyphrase = ''):
    subfolders = []
    subsubfolders = []
    filenames = os.listdir(folder)
    for filename in filenames:                                  # loop through all the files and folders
        name = os.path.join(os.path.abspath(folder), filename)
        if keyphrase in name and os.path.isdir(name):           # check whether the current object is a folder or not
            subfolders.append(name)
    if nested is None or nested > 0:
        for subfolder in subfolders:
            if nested is None:
                subsubfolders = subsubfolders + get_subfolders(subfolder)
            else:
                subsubfolders = subsubfolders + get_subfolders(subfolder, nested-1)
    return subfolders + subsubfolders