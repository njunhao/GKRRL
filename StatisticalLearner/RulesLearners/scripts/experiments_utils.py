#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:58:30 2019

@author: alvin
"""

import os
import subprocess
import shutil
import operator


if os.getcwd().find('/RulesLearners/') >= 0:
    root_path = os.getcwd()[:os.getcwd().find('/RulesLearners/')+len('/RulesLearners/')]
elif os.getcwd().find('/RulesLearners') >= 0:
    root_path = os.getcwd()[:os.getcwd().find('/RulesLearners')+len('/RulesLearners')]
else:
    raise("Unable to determine library path, current directory is " + os.getcwd())

logger_filename = 'logger.conf'
config_filename = 'config.cfg'
logfile = 'ruleslearner.log'
bin_path = root_path + '/bin/ruleslearners'
work_path = root_path + '/log/'
log_path = work_path + '/current'
logger_path = root_path + '/scripts/' + logger_filename
results_folder = '/results'

# files to be saved
results_files = [logfile, config_filename, 'learned_rules.dat', 'learner_output.log', 'learned_domain.rddl', 'learned_domain.ppddl', 'learned_domain_preselection']

# most of the options are deprecated as we use config.cfg to pass in parameters instead
# tuple: (type, default value)
# if type starts with -- then this is to pass in as arguments when calling mbrrl binary as optional arguments
# if type is numeric, then this is to pass in as non-optional arguments with the # indicating the position of the argument when calling mbrrl binary
# if type is 'config', then this is used to overwrite .cfg config_file that is used for experiments, the key must match the parameter name in .cfg
# if type is None, then this is not passed to CPP in any way
def_configs = {
        'learner': 'pasula',
        'beam_search_branch': 1,
        'rddl_write_precondition': 'false',

        'ppddl_domain_file': None,
        'ppddl_problem_template_file': None,

        'transitions_file': 'transitions.dat',
        'all_transitions_file': 'transitions_all.dat',
        'transitions_tmp_file': 'transitions_tmp.dat',
        'learner_conf': log_path+'/'+logger_filename,
        'ppddl_learned_domain_file': 'learned_domain.ppddl',
        'rules_path': 'learned_rules.dat',

        'lfit_path': root_path+'/bin/lfit',
        'pasula_path': root_path+'/bin/pasula_learner',

        'lfit_learner_max_action_variables': 4,
        'lfit_learner_max_preconditions': 5,
        'lfit_learner_optimal': 'false',
        'lfit_learner_use_subsumption_tree': 'false',
        'lfit_learner_conflicts_heuristic_max_iterations': 50,
        'lfit_learner_conflicts_heuristic_max_rules_per_iter': 1000,
        'lfit_learner_score_optimistic_value': 1.0,
        'lfit_learner_score_use_confidence': 'true',
        'lfit_learner_score_regularization_scaling': 0.02,
        'lfit_learner_score_confidence_interval': 0.1,
        'lfit_learner_aggressive_prunning': 'true',
        'max_transitions_per_action': 100,
        'pasula_alpha_pen': 0.25,
        'pasula_noise_lower_bound': 1e-9,
        'pasula_noise_lower_bound_default_rule': 1e-11
}


# -----------------------------
# -----------------------------
# -----------------------------
#       RUN COMMANDS
# -----------------------------
# -----------------------------
# -----------------------------

def run(**kwargs):
    if kwargs.get('ppddl_domain_file', None) is None:
        kwargs['ppddl_domain_file'] = kwargs['domain'] + '_mdp_template.pddl'
    if kwargs.get('ppddl_problem_template_file', None) is None:
        kwargs['ppddl_problem_template_file'] = kwargs['domain'] + '_inst_mdp_template.pddl'
    if kwargs.get('mapping_file', None) is None:
        kwargs['mapping_file'] = kwargs['domain'] + '_known_mappings.dat'
    current_results_files = results_files #+ [kwargs['all_transitions_file']]   # do not copy transitions file
    
    if kwargs['learner']:
        print("Make sure that prada.so is added to LD_LIBRARY_PATH:\n     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + root_path + "../prada/lib/")

    # clear folder first
    active_log_path = log_path + '_' + kwargs['module']
    active_results_folder = results_folder + '_' + kwargs['module']
    kwargs['learner_conf'] = active_log_path+'/'+logger_filename
    if not os.path.exists(active_log_path):
        os.makedirs(active_log_path)
    elif kwargs.get('clear_all_files', True):
        remove_all_files_in_folder(active_log_path)

    # copy files
    input_files = [kwargs['ppddl_domain_file'], kwargs['ppddl_problem_template_file'], kwargs['mapping_file'], config_filename, kwargs['all_transitions_file']]
    copy_files(input_files, work_path+'/'+kwargs['domain'], active_log_path)
    copy_files([logger_path], root_path, active_log_path, True)

    # retain only filenames before modifying config files which will use these values
    kwargs['ppddl_domain_file'] = getFilename(kwargs['ppddl_domain_file'])
    kwargs['ppddl_problem_template_file'] = getFilename(kwargs['ppddl_problem_template_file'])
    kwargs['all_transitions_file'] = getFilename(kwargs['all_transitions_file'])
    
    # modify filenames and paths in config files
    modify_config(active_log_path+'/'+config_filename, **kwargs)
    modify_logger_conf(active_log_path+'/'+logger_filename, active_log_path+'/'+logfile)

    # get commands
    if kwargs.get('action', None):
        cmdline = bin_path + ' ' + active_log_path+'/'+config_filename + ' ' + active_log_path + ' ' + kwargs['action']   # excluded last arg for action
    else:
        cmdline = bin_path + ' ' + active_log_path+'/'+config_filename + ' ' + active_log_path                            # excluded last arg for action
    
    # run executable
    try:
        res = subprocess.call(cmdline, shell=True)
        if (res != 0):
            print("Unexpected error")
    except KeyboardInterrupt:
        print("\nUser terminated program!")
        return 0
    except:
        print("\nMain Program crashed due to unknown reason!")
        return 0

    results_path = finish_experiment(work_path+active_results_folder, active_log_path, kwargs['domain'], current_results_files)
    f = open(work_path+active_results_folder+'/summary.log', 'a+')
    f.write('\n--------------------\nFolder: ' + results_path)
    f.write(kwargs['msg'])
    f.close()
    return 1


def finish_experiment(root_path, src_path, dst_folder, save_files):
    dst_folder += '_'
#    ps=os.popen('ls '+root_path+' | grep ' + current_result_dir + ' | cut -d "_" -f4 2>/dev/null')
    ps=os.popen('ls '+root_path+' | grep ' + dst_folder)
    folders=ps.readlines()
    if len(folders):
        num=max([int(x[-4:]) for x in folders])
    else:
        num=0
    num=num+1
    num_str = "%04d" % (num)
    
    # create folder results/domain/experiment_problem_num
    new_path = root_path + '/' + dst_folder + num_str
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    copy_files(save_files, src_path, new_path)
    shutil.rmtree(src_path)
    print("Finished experiment.")
    return new_path


# -----------------------------
# -----------------------------
# -----------------------------
#       PRE-RUN FUNCTIONS
# -----------------------------
# -----------------------------
# -----------------------------

def modify_config(filename, **kwargs):
    def get_parameter_name(line):
        return line[0 : line.find('=')].strip()

    def form_new_line(param, value, line = ''):
        if isinstance(value, str):
            return param + ' = ' + value + '\n'
        elif isinstance(value, bool):
            if value:
                return param + ' = true\n'
            else:
                return param + ' = false\n'
        elif isinstance(value, list):
            if value == []:
                return line
            else:
                return param + ' = ' + list2string(value, sort=False, linebreak=False, delimiter=' ') + '\n'
        else:
            return param + ' = ' + str(value) + '\n'

    destination = open(filename+'~', 'w')   # temp file
    source = open(filename, 'r')
    list_of_params_written = []
    for line in source:
        if line != '' and line[0] != '#':
            param = get_parameter_name(line)
            if param in kwargs:
                # overwrite parameter value
                line = form_new_line(param, kwargs[param], line)
                list_of_params_written.append(param)
        destination.write(line)
    
    # now check for remaining parameters in kwargs that were not yet written
    # this happens if .cfg did not have these parameters to be over-written
    write_comment = True
    for param, value in sorted(kwargs.items(), key=operator.itemgetter(0)):     # write params in alphabetical order for consistency
        if param not in def_configs.keys():
            continue                                                            # param is not a config
        if value is None or (isinstance(value, list) and not value):            # skip None and empty lists
            continue
        if param not in list_of_params_written:
            if write_comment:
                destination.write('\n\n# Configs from Python\n')
                write_comment = False
            destination.write(form_new_line(param, kwargs[param]))

    # close files and overwrite original .cfg file
    source.close()
    destination.close()
    shutil.move(filename+'~', filename)


def modify_logger_conf(filename, logfilename):
    PHRASE = "    FILENAME                =   "
    destination = open(filename+'~', 'w')   # temp file
    source = open(filename, 'r')
    for line in source:
        if line.find(PHRASE.strip()) > 0:
            line = PHRASE+ "\"" + '/' + logfilename + "\"\n"
        destination.write(line)
    # close files and overwrite original .cfg file
    source.close()
    destination.close()
    shutil.move(filename+'~', filename)


# -----------------------------
# -----------------------------
# -----------------------------
#       UTILITY
# -----------------------------
# -----------------------------
# -----------------------------

def xstr(s):
    return 'none' if s is None else str(s)


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


def getFilename(file):
    return file[file.rfind('/')+1 :]


# -----------------------------
# -----------------------------
# -----------------------------
#       FILES UTILITY
# -----------------------------
# -----------------------------
# -----------------------------


# clone folders in orig_path to dest_path, including files in these folders
def clone_folders(folders, orig_path, dest_path):
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    for folder in folders:
        if not os.path.isdir(dest_path+folder):
            os.makedirs(dest_path+folder)
        if os.path.isdir(orig_path+folder):
            files = [f for f in os.listdir(orig_path+folder) if os.path.isfile(os.path.join(orig_path+folder, f) )]
            copy_files(files, orig_path+folder, dest_path+folder)


def copy_files(files, orig_path, dest_path, verbose = True):
    for a_file in files:
        try:
            shutil.copy2(orig_path + '/' + a_file, dest_path)
        except:
            try:
                shutil.copy2(a_file, dest_path)
            except:
                if verbose:
                    print("Warning: Couldn't copy " + a_file)

# create empty files
def create_files(files, path):
    for a_file in files:
        open(path + '/' + a_file, 'w').close()


def move_files(files, orig_path, dest_path, verbose = True):
    for a_file in files:
        try:
            shutil.move(orig_path + '/' + a_file, dest_path)
        except:
            try:
                shutil.move(a_file, dest_path)
            except:
                if verbose:
                    print("Warning: Couldn't move " + a_file)


def remove_files(files, path = '', verbose = True):
    if not isinstance(files, list):
        files = [files]
    for a_file in files:
        try:
            os.remove(path + '/' + a_file)
        except:
            if verbose:
                print("Warning: Couldn't remove " + a_file)


def remove_all_files_in_folder(folder, delete_subfolder = False):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path) and delete_subfolder:
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def get_files_from_folder(folder, filename):
    files = []
    subfolders = os.listdir(folder)
    # print(subfolders)
    for subfolder in subfolders:
        subfolder = folder+'/'+subfolder
        if os.path.isdir(subfolder):
            if os.path.isfile( os.path.join(folder, subfolder, filename) ):
                files.append(os.path.join(folder, subfolder, filename))
    return files




def main():
    print('Nothing to do')

if __name__ == "__main__":
    main()