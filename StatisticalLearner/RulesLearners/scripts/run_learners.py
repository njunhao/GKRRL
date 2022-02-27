#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:46:20 2019

@author: alvin
"""

import sys
import importlib
import experiments_utils as exp_utils  # edit this file to specify filepaths and def arguments

clear_all_files = True                 # True to delete all files in working folder at the start (only set to False if a file in the folder is to be imported by executable)


def create_experiments_combinations():
    return [(domain, learner, transitions_file, config) \
            for domain in exp_settings.domains \
            for learner in exp_settings.learners \
            for transitions_file in exp_settings.transitions_files[domain] \
            for config in exp_settings.configs]


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception('./run_learners.py [name of settings]')
    
    module_name = 'settings_' + sys.argv[1]
    exp_settings = importlib.import_module(module_name)
    
    for domain, learner, transitions_file, config in create_experiments_combinations():
        # initialize
        kwargs = {}
        kwargs = exp_utils.def_configs.copy()
        kwargs.update(config)
        kwargs['module'] = sys.argv[1]
        kwargs['domain'] = domain
        kwargs['learner'] = learner
        kwargs['all_transitions_file'] = transitions_file
        kwargs['clear_all_files'] = clear_all_files
        kwargs['action'] = exp_settings.actions[kwargs['domain']]
        msg = '\n    Domain: ' + domain + ', Learner: ' + learner + ', Transitions: ' + transitions_file + '\n    Config: '
        for key, value in config.items():
            msg += '\n         ' + key + ': ' + str(value)

        # run client for #num_reps times
        for i in range(exp_settings.num_reps):
            # run client
            msg2 = '\n    Repetition #' + str(i+1) + '/' + str(exp_settings.num_reps)
            kwargs['msg'] = msg + msg2
            print(kwargs['msg'])
            status = exp_utils.run(**kwargs)
            if status == 0:
                sys.exit()