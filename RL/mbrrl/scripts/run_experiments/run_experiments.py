#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:46:20 2019

@author: alvin
"""

import os.path
import sys
import random
import shutil
import importlib
import math
import domains_utils                    # edit this file to specify folders and files for .rddl domains
import experiments_utils as exp_utils   # edit this file to specify filepaths and def arguments
import random_problem_generator.rpg as rpg

client_sleep = 0

def create_experiments_combinations(fa_index = None):
    setup = []      # problem, learner, exp, initial_domain
    initial_domains = exp_settings.initial_domains
    if isinstance(initial_domains, list) and len(initial_domains) == 1:
        if isinstance(initial_domains[0], str):
            initial_domains = [initial_domains]                     # wrap this into a list of list
    if initial_domains and exp_settings.intrinsic_reward_types:     # non-empty list
        setup = [(problem, learners, exp, model, initial_domain, intrinsic_reward_types) \
                    for problem in exp_settings.problems \
                    for learners in exp_settings.learners \
                    for exp in exp_settings.experiences \
                    for model in exp_settings.model_representations \
                    for initial_domain in initial_domains[exp_settings.problems.index(problem)] \
                    for intrinsic_reward_types in exp_settings.intrinsic_reward_types]
    elif initial_domains:
        setup = [(problem, learners, exp, model, initial_domain, None) \
                    for problem in exp_settings.problems \
                    for learners in exp_settings.learners \
                    for exp in exp_settings.experiences \
                    for model in exp_settings.model_representations \
                    for initial_domain in initial_domains[exp_settings.problems.index(problem)]]
    elif exp_settings.intrinsic_reward_types:
        setup = [(problem, learners, exp, model, None, intrinsic_reward_types) \
                    for problem in exp_settings.problems \
                    for learners in exp_settings.learners \
                    for exp in exp_settings.experiences \
                    for model in exp_settings.model_representations \
                    for intrinsic_reward_types in exp_settings.intrinsic_reward_types]
    else:
        setup = [(problem, learners, exp, model, None, None) \
                    for problem in exp_settings.problems \
                    for learners in exp_settings.learners \
                    for exp in exp_settings.experiences \
                    for model in exp_settings.model_representations]

    # combination = {problem, planner, learners, policy, exp, initial_domain, FA, plan_rollout, intrinsic reward}
    combinations = []
    
    for problem, learners, exp, model, initial_domain, intrinsic_reward_types in setup:
        if len(problem) != 2:
            raise Exception('Problem instances should be a tuple of this format: (domain name, problem instance)')
        function_approximations = exp_settings.function_approximations
        if problem[0] in exp_settings.keyed_function_approximations:            # problem[0] is domain
            function_approximations = exp_settings.keyed_function_approximations[problem[0]]
        else:
            if isinstance(problem[1], list):
                pass
                # print("WARNING: Can't use keyed function approximations if more than one problem instance per session")
            elif problem in exp_settings.keyed_function_approximations:
                function_approximations = exp_settings.keyed_function_approximations[problem]
        # user input an index (fa_index) for function_approximations
        # this must be done here as we might be using keyed_function_approximations
        if fa_index is not None:
            try:
                if fa_index > len(function_approximations):
                    raise Exception('User input of ' + str(fa_index) + ' exceeds the size of function_approximations (' + str(len(exp_settings.function_approximations )) + ')')
                else:
                    function_approximations = function_approximations[fa_index]
                if not isinstance(function_approximations, list):
                    function_approximations = [function_approximations]
            except:
                raise 'Unable to set configuration for function_approximations'

        for planner in exp_settings.planners:
            if planner in exp_utils.alias['prost']:
                if exp_settings.plan_rollouts:
                    for plan_rollout in exp_settings.plan_rollouts:
                        combinations.append([problem, planner, learners, None, exp, model, initial_domain, None, plan_rollout, intrinsic_reward_types])
                else:
                    combinations.append([problem, planner, learners, None, exp, model, initial_domain, None, None, intrinsic_reward_types])
            elif planner in exp_utils.alias['rmax'] or planner in exp_utils.alias['vmax']:
                # if 'lfit' in learners or 'pasula' in learners:
                if exp_settings.plan_rollouts:
                    for plan_rollout in exp_settings.plan_rollouts:
                        combinations.append([problem, planner, learners, 'greedy', exp, model, initial_domain, None, plan_rollout, intrinsic_reward_types])
                else:
                    combinations.append([problem, planner, learners, 'greedy', exp, model, initial_domain, None, None, intrinsic_reward_types])
            else:
                for policy in exp_settings.policies:
                    for fa in function_approximations:
                        if not isinstance(fa, list):                    # to handle the case where exp_settings.function_approximations is a list of list
                            fa = [fa]
                        for fa_ in fa:
                            # if ('lfit' in learners or 'pasula' in learners) and exp_settings.plan_rollouts:
                            if exp_settings.plan_rollouts:
                                for plan_rollout in exp_settings.plan_rollouts:
                                    combinations.append([problem, planner, learners, policy, exp, model, initial_domain, fa_, plan_rollout, intrinsic_reward_types])
                            else:
                                combinations.append([problem, planner, learners, policy, exp, model, initial_domain, fa_, None, intrinsic_reward_types])
    if exp_settings.plan_rollouts:
        print('Created ' + str(len(combinations)) + ' combination(s) with ' + str(len(exp_settings.planners)) + ' planners, ' + str(len(exp_settings.policies)) + ' policies, ' + str(len(function_approximations)) + ' LFA' + str(len(exp_settings.plan_rollouts)) + ' rollouts')
    else:
        print('Created ' + str(len(combinations)) + ' combination(s) with ' + str(len(exp_settings.planners)) + ' planners, ' + str(len(exp_settings.policies)) + ' policies, ' + str(len(function_approximations)) + ' LFA')
    return combinations


def interpret_function_approximation(fa, **kwargs):
    def is_int(value):
        try:
            value = int(value)
        except ValueError:
            return False
        return True

    def read_extension(value, **kwargs):
        value = value.lower()
        if kwargs.get('lfa_base_features', None) is None:
            kwargs['lfa_base_features'] = None
        hierarchy = None
        for v in exp_utils.options['lfa_base_features']:
            if v in value:
                kwargs['lfa_base_features'] = v
                value = value.replace(v, '')
                break
        if kwargs['lfa_base_features'] is None:
            raise Exception('Unrecognized extension for ''lfa_base_features'': ' + value)
        for char in value:
            if is_int(char):
                hierarchy = int(char)
            if 'p' in char.lower():
                kwargs['lfa_aggressive_pruning'] = True
            if 'l' in char.lower():
                kwargs['lfa_first_order_features'] = True
            if 'a' in char.lower():
                kwargs['lfa_asymmetric_update'] = True
            if 's' in char.lower():
                if kwargs.get('lfa_use_non_fluents', 0) < 1:
                    kwargs['lfa_use_non_fluents'] = 1
            if 'n' in char.lower():
                kwargs['lfa_use_neg_features'] = True
            if 'd' in char.lower():
                kwargs['lfa_use_decoupled_weights'] = True
        if hierarchy and kwargs['lfa_base_features'] == 'cpf':
            kwargs['lfa_base_features'] += '_' + str(hierarchy)
        return kwargs

    if isinstance(fa, tuple):
        for value in fa:
            if isinstance(value, tuple):
                if len(value) == 2 and isinstance(value[0], str):
                    # first element is key, second element is value
                    kwargs[value[0]] = value[1]
                else:
                    print(value)
                    raise Exception('Unrecognized format for function approximation')
            elif value in exp_utils.options['function_approximations']:
                kwargs['function_approximation'] = value
            elif value in exp_utils.options['features_learners']:
                kwargs['features_learner'] = value
            elif isinstance(value, str):
                value_split = value.split('-')
                if any(s in value_split for s in \
                    exp_utils.options['lfa_substitutions_operator'] + \
                    exp_utils.options['lfa_substitutions_metric'] + \
                    exp_utils.options['lfa_substitutions_context']):
                    givenContext = False
                    if 'given-' in value:
                        value = value.replace('given-', '')
                        givenContext = True
                    elif '-given' in value:
                        value = value.replace('-given', '')
                        givenContext = True
                    if givenContext:
                        if exp_settings.client_args.get('lfa_goal_sequence', None):
                            kwargs['lfa_goal_sequence'] = exp_settings.client_args['lfa_goal_sequence']
                        elif kwargs.get('given_order_key', None) in exp_utils.lfa_goal_sequence:
                            kwargs['lfa_goal_sequence'] = exp_utils.lfa_goal_sequence[kwargs['given_order_key']]
                        else:
                            # TODO
                            givenContext = False
                            if kwargs.get('given_order_key', None):
                                raise Exception('Given ordered context for problem ' + kwargs['given_order_key'] + ' is not defined')
                                # exp_utils.print_msg(kwargs['verbose_msg'], 'Given ordered context for problem ' + kwargs['given_order_key'] + ' is not defined')
                            else:
                                raise Exception('Problem instance not defined, unable to provide given ordered context')
                    kwargs['lfa_free_var_substitution'] = value
                else:
                    kwargs = read_extension(value, **kwargs)
            elif isinstance(value, bool):
                kwargs['lfa_common_learning'] = value
    else:
        kwargs['function_approximation'] = fa

    if kwargs.get('ifdd_initial_feature_size', 0) > kwargs.get('ifdd_max_feature_size', 0):
        exp_utils.print_msg(kwargs['verbose_msg'], 'ifdd_initial_feature_size > ifdd_max_feature_size, no features will be learned')
    return kwargs


def check_settings(**kwargs):    
    if kwargs['learner'] == '':
        kwargs['learning'] = False
    else:
        kwargs['learning'] = True
        if 'lfit' in kwargs['learner'] or 'pasula' in kwargs['learner']:
            if kwargs.get('max_round_for_learning', None) is None or kwargs['max_round_for_learning'] <= 0:
                exp_utils.print_msg(kwargs['verbose_msg'], 'Model learning (max_round_for_learning <=0) is disabled when not using true domain')
        else:
            kwargs['max_round_for_learning'] = None

    using_true_domain = True
    if 'initial_domain' in kwargs:
        if kwargs.get('initial_domain', None) is not None and kwargs['initial_domain'] != "":
            using_true_domain = False
            if kwargs['planner'] in exp_utils.alias['prost']:
                exp_utils.print_msg(kwargs['verbose_msg'], 'Do not use PROST if using approx. domain, PROST will pick noop() all the time')
            # if kwargs['prune']:
            #     exp_utils.print_msg(kwargs['verbose_msg'], 'Must not prune if ground truth domain is not used --> disable pruning')
            #     kwargs['prune'] = False
            if not kwargs['learning']:
                exp_utils.print_msg(kwargs['verbose_msg'], 'No learner specified when not using true domain')

    if using_true_domain and kwargs['learning']:
        kwargs['learner']= []
        kwargs['learning'] = False
        kwargs['max_round_for_learning'] = None
        exp_utils.print_msg(kwargs['verbose_msg'], 'If true initial model is provided, then model learning is not required --> disable model learner')
        if kwargs.get('import_transition_reset', None):
            kwargs['import_transition_reset'] = False
            exp_utils.print_msg(kwargs['verbose_msg'], 'If true initial model is provided, then model learning is not required --> disable import_transition_reset')
        

    # if kwargs['learn_from_failure']:
    #     kwargs['reward_for_failed_execution'] = 0
    #     exp_utils.print_msg(kwargs['verbose_msg'], 'Do not need to assign reward for failed execution if using LfF --> set reward_for_failed_execution = 0')
    if kwargs['learning']:
        if kwargs['prune']:
            exp_utils.print_msg(kwargs['verbose_msg'], 'Must not prune if learner is given, this will remove state fluents --> disable pruning')
            kwargs['prune'] = False
    
    if not using_true_domain and kwargs.get('rddl_write_precondition', False) and not kwargs.get('learn_from_failure', False) and not kwargs['always_update_q']:
        kwargs['always_update_q'] = True
        exp_utils.print_msg(kwargs['verbose_msg'], 'Must always update Q-value if precondition is unknown and not using LfF --> always_update_q = True')

    if kwargs.get('prune', None):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Using PROST pruning, this may prune state variables and cause state to remain unchanged even when it has changed')
    
    # if kwargs.get('beam_search_branch', None) and kwargs.get('num_hypothesis_domains', None):
    #     if kwargs['beam_search_branch'] < kwargs['num_hypothesis_domains']:
    #         exp_utils.print_msg(kwargs['verbose_msg'], 'beam_search_branch should be >= num_hypothesis_domains --> set num_hypothesis_domains = beam_search_branch')
    #         kwargs['num_hypothesis_domains'] = kwargs['beam_search_branch']
    
    if kwargs['planner'] in exp_utils.alias['rmax'] or kwargs['planner'] in exp_utils.alias['vmax']:
        if kwargs.get('intrinsic_reward_types', None):
            if 'rmax' in kwargs['intrinsic_reward_types']:
                if isinstance(kwargs['intrinsic_reward_types'], list):
                    kwargs['intrinsic_reward_types'].remove('rmax')
                else:
                    kwargs['intrinsic_reward_types'] = None
                exp_utils.print_msg(kwargs['verbose_msg'], 'Cannot use intrinsic_reward_types = rmax if planner is RMAX or VMAX --> remove rmax from intrinsic_reward_types')
            # if 'relational_rmax' in kwargs['intrinsic_reward_types']:
            #     if isinstance(kwargs['intrinsic_reward_types'], list):
            #         kwargs['intrinsic_reward_types'].remove('relational_rmax')
            #     else:
            #         kwargs['intrinsic_reward_types'] = None
            #     exp_utils.print_msg(kwargs['verbose_msg'], 'Cannot use intrinsic_reward_types = relational_rmax if planner is RMAX or VMAX --> remove relational_rmax from intrinsic_reward_types')
        
        # if kwargs['discount'] != 1:
        #     exp_utils.print_msg(kwargs['verbose_msg'], 'No discount allowed for RMAX and VMAX --> set discount = 1.0')
        #     kwargs['discount'] = 1

    # if kwargs.get('intrinsic_reward_types', None):
    #     if 'rmax' in kwargs['intrinsic_reward_types'] and 'relational_rmax' in kwargs['intrinsic_reward_types']:
    #         if kwargs['experience'] == 'relational':
    #             kwargs['intrinsic_reward_types'].remove('rmax')
    #             exp_utils.print_msg(kwargs['verbose_msg'], 'Cannot use intrinsic_reward_types = rmax and relational_rmax at the same time --> remove rmax from intrinsic_reward_types')
    #         else:
    #             kwargs['intrinsic_reward_types'].remove('relational_rmax')
    #             exp_utils.print_msg(kwargs['verbose_msg'], 'Cannot use intrinsic_reward_types = rmax and relational_rmax at the same time --> remove relational_rmax from intrinsic_reward_types')
        
    #     if 'relational_rmax' in kwargs['intrinsic_reward_types'] and kwargs['experience'] != 'relational':
    #         if isinstance(kwargs['intrinsic_reward_types'], list):
    #             kwargs['intrinsic_reward_types'].remove('relational_rmax')
    #             kwargs['intrinsic_reward_types'].append('rmax')
    #         else:
    #             kwargs['intrinsic_reward_types'] = 'rmax'
    #         exp_utils.print_msg(kwargs['verbose_msg'], 'Cannot use intrinsic_reward_types = relational_rmax if experience is not relational --> replace relational_rmax with rmax')

    if kwargs.get('multi_planning', None):
        if kwargs['planner'] in exp_utils.alias['prost'] and 'hybrid' in kwargs['multi_planning']:
            exp_utils.print_msg(kwargs['verbose_msg'], 'Using hybrid planning and PROST is not implemented --> disable multi_planning')
            kwargs['multi_planning'] = None
            kwargs['plan_rollout_horizon'] = 0
        if not kwargs.get('plan_rollout_horizon', None) or kwargs.get('plan_rollout_horizon', None) == 0:
            exp_utils.print_msg(kwargs['verbose_msg'], 'Rollout horizon must be > 0 if using MPS --> set plan_rollout_horizon = 1')
            kwargs['plan_rollout_horizon'] = 1
        if kwargs['multi_planning'] == 'safe' or 'hybrid' in kwargs['multi_planning']:
            if kwargs.get('plan_rollout_horizon', None) and kwargs['plan_rollout_horizon'] > 1:
                exp_utils.print_msg(kwargs['verbose_msg'], 'plan_rollout_horizon > 1 is pointless if using semi-hybrid, hybrid or safe MPS')
                # kwargs['plan_rollout_horizon'] = 1
    else:
        if kwargs.get('plan_rollout_horizon', None) and kwargs['plan_rollout_horizon'] > 1:
            exp_utils.print_msg(kwargs['verbose_msg'], 'plan_rollout_horizon > 1 is pointless if not using MPS')

    if kwargs.get('use_local_min_detection', None):
	    if kwargs.get('local_min_non_goal_penalty', None):
	        # if kwargs['planner'] is not 'ql' and kwargs['planner'] is not 'sarsal':
	        #     kwargs['local_min_non_goal_penalty'] = None
	        #     exp_utils.print_msg(kwargs['verbose_msg'], 'If not using Q(lambda) or SARSA(lambda), then local_min_non_goal_penalty should not be used --> set local_min_non_goal_penalty = None')
	        if kwargs['local_min_non_goal_penalty'] > 0:
	            kwargs['local_min_non_goal_penalty'] = -kwargs['local_min_non_goal_penalty']
	            exp_utils.print_msg(kwargs['verbose_msg'], 'local_min_non_goal_penalty should be < 0 --> set local_min_non_goal_penalty = ' + str(kwargs['local_min_non_goal_penalty']))

    if kwargs.get('intrinsic_reward_types', None):
        remove_learner_intrinsic_reward = False
        if 'learner' in kwargs['intrinsic_reward_types']:
            if 'lfit' not in kwargs['learner'] and 'pasula' not in kwargs['learner']:
                remove_learner_intrinsic_reward = True
                exp_utils.print_msg(kwargs['verbose_msg'], 'Model learner is not in use --> disable ' + exp_utils.options['intrinsic_reward_types'][2] + ' intrinsic reward')
            # else:
            #     value = kwargs.get('max_intrinsic_reward', None)
            #     if value is None:
            #         remove_learner_intrinsic_reward = True
            #         exp_utils.print_msg(kwargs['verbose_msg'], 'max_intrinsic_reward must be defined --> disable ' + exp_utils.options['intrinsic_reward_types'][2] + ' intrinsic reward')
            #     elif value == 0.0:
            #         remove_learner_intrinsic_reward = True
            #         exp_utils.print_msg(kwargs['verbose_msg'], 'max_intrinsic_reward must be > 0.0 --> disable ' + exp_utils.options['intrinsic_reward_types'][2] + ' intrinsic reward')
            if remove_learner_intrinsic_reward:
                if isinstance(kwargs['intrinsic_reward_types'], list):
                    kwargs['intrinsic_reward_types'].remove('learner')
                else:
                    kwargs['intrinsic_reward_types'] = None

    if kwargs.get('import_transition_reset', None) and kwargs.get('import_transition_file', None) and not kwargs['learner']:
        raise Exception('If importing transitions and import_transition_reset is True, then model learner must be defined')

    if kwargs.get('multi_planning', None):
        if not kwargs['use_model_for_prediction']:
            exp_utils.print_msg(kwargs['verbose_msg'], 'Multi-Model Planning can only be used if use_model_for_prediction = True')
        if kwargs['model_representation'] != 'dbn':
            exp_utils.print_msg(kwargs['verbose_msg'], 'Warnign: Multi-Model Planning should be used with DBN model representation')
            # exp_utils.print_msg(kwargs['verbose_msg'], 'Multi-Model Planning can only be used if using DBN model representation --> model_representation = DBN')
            # kwargs['model_representation'] = 'dbn'

    if not kwargs.get('online_q_update', True):
        q_update_is_done = False
        if kwargs.get('import_transition_file', None) and kwargs.get('import_transition_reset', None) == False:
            exp_utils.print_msg(kwargs['verbose_msg'], 'online_q_update is false, Q-function will be trained with imported transition file')
            q_update_is_done = True
        if kwargs.get('import_qvalue', None):
            exp_utils.print_msg(kwargs['verbose_msg'], 'online_q_update is false, Q-function is imported')
            q_update_is_done = True
        if kwargs.get('self_play_horizon', 0) > 0 and kwargs.get('self_play_repetitions', 0) > 0:
            if kwargs['model_representation'] != 'dbn':
                exp_utils.print_msg(kwargs['verbose_msg'], 'online_q_update is false and Q-function cannot be trained with self-play at the start if not using DBN model representation')
                q_update_is_done = False
            else:
                exp_utils.print_msg(kwargs['verbose_msg'], 'online_q_update is false, Q-function will be trained with self-play at the start')
                q_update_is_done = True
        if not q_update_is_done:
            exp_utils.print_msg(kwargs['verbose_msg'], 'online_q_update is false, Q-function will not be trained at all --> set online_q_update = True')
            kwargs['online_q_update'] = True

    if kwargs.get('self_play_horizon', 0) > 0 and kwargs.get('self_play_repetitions', 0) > 0:
        if not kwargs['use_model_for_prediction']:
            exp_utils.print_msg(kwargs['verbose_msg'], 'Self-play can only be done if use_model_for_prediction = True')
        elif kwargs['model_representation'] != 'dbn':
            exp_utils.print_msg(kwargs['verbose_msg'], 'Self-play can only be done if using DBN model representation or given transitions data')

    if kwargs.get('mve_horizon', 0) > 0 and not kwargs['use_model_for_prediction']:
        exp_utils.print_msg(kwargs['verbose_msg'], 'MVE can only be done if use_model_for_prediction = True')

    # make sure there are no spaces in file paths
    if kwargs.get('import_policy', None) is not None and ' ' in kwargs.get('import_policy', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (import_policy)')
    if kwargs.get('export_policy', None) is not None and ' ' in kwargs.get('export_policy', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (export_policy)')
    if kwargs.get('import_qvalue', None) is not None and ' ' in kwargs.get('import_qvalue', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (import_qvalue)')
    if kwargs.get('export_qvalue', None) is not None and ' ' in kwargs.get('export_qvalue', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (export_qvalue)')
    if kwargs.get('export_intrinsic_reward', None) is not None and ' ' in kwargs.get('export_intrinsic_reward', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (export_intrinsic_reward)')
    if kwargs.get('plans_file', None) is not None and ' ' in kwargs.get('plans_file', ''):
        exp_utils.print_msg(kwargs['verbose_msg'], 'Spaces in file path might cause issues (plans_file)')
    
    # check FA 
    if kwargs.get('function_approximation', None):
        if kwargs['function_approximation'] != 'linear':
            if kwargs.get('lfa_aggressive_pruning', None):
                kwargs['lfa_aggressive_pruning'] = False
                exp_utils.print_msg(kwargs['verbose_msg'], 'lfa_aggressive_pruning is only applicable for LFA --> set lfa_aggressive_pruning = False')
            if kwargs.get('lfa_first_order_features', None):
                exp_utils.print_msg(kwargs['verbose_msg'], 'lfa_first_order_features is only applicable for LFA --> set lfa_first_order_features = False')
                kwargs['lfa_first_order_features'] = False
            if kwargs.get('lfa_asymmetric_update', None):
                kwargs['lfa_asymmetric_update'] = False
                exp_utils.print_msg(kwargs['verbose_msg'], 'lfa_asymmetric_update is only applicable for LFA --> set lfa_asymmetric_update = False')
            if kwargs.get('lfa_use_non_fluents', None):
                kwargs['lfa_use_non_fluents'] = 0
                exp_utils.print_msg(kwargs['verbose_msg'], 'lfa_use_non_fluents is only applicable for LFA --> set lfa_use_non_fluents = 0')
            if kwargs.get('lfa_use_neg_features', None):
                kwargs['lfa_use_neg_features'] = False
                exp_utils.print_msg(kwargs['verbose_msg'], 'lfa_use_neg_features is only applicable for LFA --> set lfa_use_neg_features = False')
        
        if kwargs['function_approximation'] == 'linear':
            if kwargs.get('lfa_first_order_features', None):
                # if kwargs.get('lfa_aggressive_pruning', None):
                #     kwargs['lfa_aggressive_pruning'] = False
                #     exp_utils.print_msg(kwargs['verbose_msg'], 'If using lfa_first_order_features, then lfa_aggressive_pruning is already used --> set lfa_aggressive_pruning = False')
                if not kwargs.get('lfa_use_non_fluents', None):
                    exp_utils.print_msg(kwargs['verbose_msg'], 'If using lfa_first_order_features, then lfa_use_non_fluents is recommended')
            if kwargs['lfa_base_features'] == 'import':
                if kwargs['problem'].count('inst') == 1:
                    qvalue_filename = kwargs.get('import_qvalue', None)
                    if qvalue_filename is None:
                        qvalue_filename = exp_utils.impt_paths['features_path'] + '/' + kwargs['problem'].strip() + '_features.txt'
                        if os.path.exists(qvalue_filename):
                            kwargs['import_qvalue'] = qvalue_filename
                        else:
                            exp_utils.print_msg(kwargs['verbose_msg'], 'function_approximation = ' + kwargs['function_approximation'] + ' requires non-existent file (' + qvalue_filename + ')')
                    elif not os.path.isfile(qvalue_filename):
                        exp_utils.print_msg(kwargs['verbose_msg'], 'function_approximation = ' + kwargs['function_approximation'] + ' requires non-existent file (' + qvalue_filename + ')')
                else:
                    exp_utils.print_msg(kwargs['verbose_msg'], 'function_approximation=' + kwargs['function_approximation'] + ' for multi-instances problems is not supported')
    return kwargs


def set_generated_files(**kwargs):
    kwargs['generated_files'] = exp_utils.generated_files['log']
    kwargs['generated_files_pattern'] = exp_utils.generated_files['pattern']
    kwargs['generated_files'] = kwargs['generated_files'] + exp_utils.generated_files['ros']
    if exp_settings.save_optional_log:
        kwargs['generated_files_pattern'] = kwargs['generated_files_pattern'] + exp_utils.generated_files['pattern_optional'] + exp_utils.generated_files['optional']
    if kwargs.get('function_approximation', None) and kwargs['function_approximation'] == 'neural_network':
        kwargs['generated_files'] = kwargs['generated_files'] + exp_utils.generated_files['opennn']
    else:
        kwargs['generated_files'] = kwargs['generated_files'] + [exp_utils.generated_files['opennn'][0]]
    if kwargs.get('import_qvalue', None):
        kwargs['import_qvalue'] = kwargs['log_path']+'/'+kwargs['import_qvalue']
    if kwargs.get('export_qvalue', None):
        kwargs['generated_files_pattern'].append(kwargs['export_qvalue'][:kwargs['export_qvalue'].find('.')]+'*')
        kwargs['export_qvalue'] = kwargs['log_path']+'/'+kwargs['export_qvalue']
    if kwargs.get('import_intrinsic_reward', None):
        kwargs['import_intrinsic_reward'] = kwargs['log_path']+'/'+kwargs['import_intrinsic_reward']
    if kwargs.get('export_intrinsic_reward', None):
        kwargs['generated_files_pattern'].append(kwargs['export_intrinsic_reward'][:kwargs['export_intrinsic_reward'].find('.')]+'*')
        kwargs['export_intrinsic_reward'] = kwargs['log_path']+'/'+kwargs['export_intrinsic_reward']
    if kwargs.get('import_policy', None):
        kwargs['import_policy'] = kwargs['log_path']+'/'+kwargs['import_policy']
    if kwargs.get('export_policy', None):
        kwargs['generated_files'].append(kwargs['export_policy'])
        kwargs['export_policy'] = kwargs['log_path']+'/'+kwargs['export_policy']
    if kwargs.get('tabu_file', None):
        kwargs['generated_files'].append(kwargs['tabu_file'])
        # kwargs['generated_files'].append(kwargs['tabu_file'][:kwargs['tabu_file'].rfind('.')]+'_generalized'+kwargs['tabu_file'][kwargs['tabu_file'].rfind('.'):])
    return kwargs


def get_imported_files(request, **kwargs):
    def get_filenames_from_folder(folder_key, filename_key, **kwargs):
        import_filenames = None
        if kwargs.get(filename_key, None):
            if kwargs.get(folder_key, None):
                if kwargs[filename_key]:
                    import_folders = kwargs[folder_key]
                    if not isinstance(import_folders, list):
                        import_folders = [import_folders]
                    for import_folder in import_folders:
                        if '*' in import_folder:
                            if kwargs.get('domain', None):
                                import_folder = import_folder.replace('*', kwargs.get('domain', ''))
                            else:
                                raise Exception("Wild character * used in client_args['" + folder_key + "'], need to define domain name")
                        filename = kwargs[filename_key].replace('*', kwargs.get('domain', ''))
                        import_filenames = exp_utils.get_files_from_folder(import_folder, filename)
                        if import_filenames:
                            import_filenames.sort()
                            if exp_settings.num_reps > len(import_filenames):
                                exp_utils.print_msg(kwargs['verbose_msg'], 'WARNING: Num of files (' + str(len(import_filenames)) + ') to import must be >= num_reps (' + str(exp_settings.num_reps) + '), repeat files')
                                import_filenames *= math.ceil(exp_settings.num_reps / len(import_filenames))
                                import_filenames = import_filenames[:exp_settings.num_reps]
                            break
                    if import_filenames is None:
                        # raise Exception('No files of name \'' + kwargs['import_intrinsic_reward'] + '\' are found in \'' + kwargs['import_knowledge_folder'] + '\'')
                        exp_utils.print_msg(kwargs['verbose_msg'], 'WARNING: No files of name \'' + filename + '\' are found in \'' + import_folder + '\'')
            elif kwargs[filename_key]:
                exp_utils.print_msg(kwargs['verbose_msg'], "WARNING: client_args['" + filename_key + "'] is defined but client_args['" + folder_key + "'] is not defined")
        else:
            # raise Exception('client_args[''tabu_file''] needs to be defined if client_args[''import_knowledge_folder''] is defined')
            exp_utils.print_msg(kwargs['verbose_msg'], "WARNING: client_args['" + filename_key + "'] is not defined but client_args['" + folder_key + "'] is defined")
        return import_filenames


    # get list of transitions files to import
    import_transitions_filenames = None
    if 'transition' in request:
        import_transitions_filenames = get_filenames_from_folder('import_transition_folder', 'import_transition_file', **kwargs)
    
    # get list of Q-function files to import
    import_qvalue_filenames = None
    if 'policy' in request:
        import_qvalue_filenames = get_filenames_from_folder('import_knowledge_folder', 'import_qvalue', **kwargs)

    # get list of RDDL files to importlib
    import_rddl_filenames = None
    if 'domain' in request:
        import_rddl_filenames_ = get_filenames_from_folder('import_rddl_folder', 'import_rddl_file', **kwargs)
        if import_rddl_filenames_:
            if kwargs['import_multi_rddl'] <= 1:
                import_rddl_filenames = import_rddl_filenames_
            elif kwargs['import_multi_rddl'] > 1:
                if kwargs['import_multi_rddl'] > len(import_rddl_filenames_):
                    raise Exception('Num of files (' + str(len(import_rddl_filenames_)) + ') to import must be >= import_multi_rddl (' + str(kwargs['import_multi_rddl']) + ')')
                else:
                    import_rddl_filenames = []
                    for i in range(exp_settings.num_reps):
                        import_rddl_filenames.append(random.sample(import_rddl_filenames_, k=kwargs['import_multi_rddl']))

    # get list of Tabu files to import
    import_tabu_filenames = None
    if 'tabu' in request:
        import_tabu_filenames = get_filenames_from_folder('import_knowledge_folder', 'tabu_file', **kwargs)

    # get list of intrinsic reward files to import
    import_intrinsic_filenames = None
    if 'intrinsic' in request:
        import_intrinsic_filenames = get_filenames_from_folder('import_knowledge_folder', 'import_intrinsic_reward', **kwargs)

    return import_transitions_filenames, import_qvalue_filenames, import_rddl_filenames, import_tabu_filenames, import_intrinsic_filenames


def instance_is_rpg(instances):
    if not isinstance(instances, list):
        instances = [instances]
    results = []
    for instance in instances:
        if '__' in instance:
            suffix = instance[instance.find('__')+2 :].split('_')
            results.append(len(suffix) > 1)
        else:
            results.append(False)
    return results

# if instance = turtlebot_survey_inst_mdp__de3_17, returns 17
def get_instance_index(instance):
    if '__' in instance:
        suffix = instance[instance.find('__')+2 :].split('_')
        if (len(suffix) > 1):
            try:
                return int(suffix[1])
            except:
                return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception('./run_experiments.py [name of experiment settings] [client or server or help] <-port num> <-problem num> <-lfa num>')
    
    module_name = 'experiments_settings_' + sys.argv[1]
    exp_settings = importlib.import_module(module_name)
    if exp_settings.initial_domains and len(exp_settings.initial_domains) < len(exp_settings.problems):
        if len(exp_settings.initial_domains) == 1:
            exp_settings.initial_domains = exp_settings.initial_domains * len(exp_settings.problems)
        else:
            raise("No. of initial_domains should match no. of problems")
    
    # get runtime parameters
    runtime_args = {
        '-ops': 'help',
        '-port': exp_settings.client_args['simulator_port'],
        '-problem': None,
        '-lfa': None,
        '-seed': None,
        '-skip_experiments': None
    }
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] in ['client', 'server', 'help']:
            runtime_args['-ops'] = sys.argv[i]
        elif sys.argv[i] in runtime_args.keys() and i+1 < len(sys.argv):
            runtime_args[sys.argv[i]] = int(sys.argv[i+1])
            i += 1

    fa_index = None
    skip_experiments = None
    for key, value in runtime_args.items():
        if value is None:
            continue
        elif key == '-lfa':
            # handle this in create_experiments_combinations() due to the use of keyed_function_approximations
            fa_index = value
        elif key == '-problem':
            try:
                if value > len(exp_settings.problems):
                    raise Exception('User input of ' + str(value) + ' exceeds the size of problems (' + str(len(exp_settings.problems )) + ')')
                exp_settings.problems = [exp_settings.problems[value]]
            except:
                raise 'Unable to set configuration for problems'
        elif key == '-seed':
            try:
                exp_settings.rpg_seed = int(value)
            except:
                raise 'Unable to set configuration for seed'
        elif key == '-skip_experiments':
            try:
                skip_experiments = int(value)
            except:
                raise 'Unable to set configuration for skip_experiments'

    runtime_args['-ops'] = runtime_args['-ops'].lower()
    benchmark_dir = exp_settings.benchmark_dir + '-' + str(runtime_args['-port'])
    if exp_settings.rpg_seed:
        random.seed(exp_settings.rpg_seed)

    if runtime_args['-ops'] == 'help':
        exp_settings.client_args['print_usage'] = True

    if not exp_settings.learners:
        exp_settings.learners = ['']

    if runtime_args['-ops'] == 'server' or exp_settings.load_problems:
        # only copy files if running server, else risk race condition
        if exp_settings.load_all_problems:
            # copy all files to benchmark_dir
            domains_utils.lsof_domains.load(folder = benchmark_dir, load_rpg = exp_settings.num_random_inst > 0 or exp_settings.random_reps)
        else:
            # domains = [p[0] if isinstance(p, tuple) else p for p in exp_settings.problems]
            domains_utils.lsof_domains.load(folder = benchmark_dir, problems = exp_settings.problems, load_rpg = exp_settings.num_random_inst > 0 or exp_settings.random_reps)

    if exp_settings.use_release_bin:
        binary_path = exp_utils.generic_files['bin_release']
    else:
        binary_path = exp_utils.generic_files['bin_debug']

    if runtime_args['-ops'] == 'client' or runtime_args['-ops'] == 'help':
        # exp_settings.client_args.update(exp_settings.algo_args)
        exp_settings.client_args['benchmark_dir'] = benchmark_dir
        exp_settings.client_args['simulator_port'] = runtime_args['-port']
        exp_settings.client_args['log_path'] = exp_utils.impt_paths['log_path'].replace('results', 'results-'+str(runtime_args['-port']))
        do_once_only = True
        combinations =  create_experiments_combinations(fa_index)

        # overwrite here
        # import_qvalue_filenames = []

        skip_combinations = []
        skip_repetitions = []
        if skip_experiments:                                                            # if cmd line specified to skip experiments
            if exp_settings.skip_experiments:                                           # if experiments_settings specified to skip experiments
                if exp_settings.num_reps == 1:
                    num_of_runs = len(combinations)
                else:
                    num_of_runs = exp_settings.num_reps
                count = 0
                skip_experiments_copy = []
                for i in range(num_of_runs):
                    if i in exp_settings.skip_experiments:
                        skip_experiments_copy.append(i)
                    elif count < skip_experiments:
                        count += 1
                        skip_experiments_copy.append(i)
                skip_experiments = skip_experiments_copy
            else:
                skip_experiments = list(range(0, skip_experiments))                     # skip according to cmd line
        else:
            skip_experiments = exp_settings.skip_experiments                            # skip according to experiments_settings
        if exp_settings.num_reps == 1:                                                  # if only one repetition, then cannot possibly skip it, so skip combination instead
            skip_combinations = skip_experiments
        else:
            skip_repetitions = skip_experiments
        
        problem_count = 0
        for problem, planner, learners, policy, exp, model, initial_domain, fa, plan_rollout, intrinsic_reward_types in combinations:
            if problem_count in skip_combinations:                                      # skip this combination, this is useful for continuing a set of experiments
                problem_count += 1
                continue
            else:
                problem_count += 1
            # initialize
            kwargs = {}
            kwargs = exp_settings.client_args.copy()
            kwargs['client_sleep'] = client_sleep
            kwargs['module_name'] = module_name+'.py'
            if exp_settings.rpg_seed:
                kwargs['seed'] = exp_settings.rpg_seed
            elif 'seed' not in kwargs:
                kwargs['seed'] = 1
            if exp_settings.description:
                kwargs['description'] = exp_settings.description
            kwargs['verbose_msg'] = []
            kwargs['bin_copy'] = binary_path+'-'+str(kwargs['simulator_port'])
            if kwargs.get('timed_constraints', None):
                kwargs['timed_constraints'] = kwargs['timed_constraints']+'/timed_constraints_'+problem[1]+'.txt'
            use_random_problem = False

            if do_once_only:
                do_once_only = False
                # copy MBRRL binary
                try:
                    if os.path.exists(kwargs['bin_copy']):
                        os.remove(kwargs['bin_copy'])
                    shutil.copy2(binary_path, kwargs['bin_copy'])
                except:
                    raise Exception('Unable to create copy of executable '+binary_path)
                    # exp_utils.print_msg(kwargs['verbose_msg'], "WARNING: Unable to create copy of executable")
                # copy python setting files
                kwargs['actual_log_path'] = kwargs['log_path']
                if exp_utils.working_path != exp_utils.mbrrl_path:
                    kwargs['actual_log_path'] = kwargs['log_path'].replace(exp_utils.working_path, exp_utils.mbrrl_path)
                if not os.path.exists(kwargs['log_path']):
                    os.makedirs(kwargs['log_path'], exist_ok=True)
                if not os.path.exists(kwargs['actual_log_path']):
                    os.makedirs(kwargs['actual_log_path'], exist_ok=True)
                shutil.copy2(kwargs['module_name'], kwargs['actual_log_path']+'/../'+kwargs['module_name'])

            if isinstance(problem, str):            # use default inst defined in .cfg
                if exp_settings.num_random_inst > 0:
                    raise Exception('Problem instance must be specified if using Random-Generated-Problems (else set num_random_inst = 0')
                kwargs['domain'] = problem
                # exp_utils.print_msg(kwargs['verbose_msg'], "WARNING: Problem instance must be specified if using given-order-context")
            elif isinstance(problem, tuple):        # overwrite inst in .cfg
                kwargs['domain'] = problem[0]
                if (len(problem) == 1) and exp_settings.num_random_inst > 0:
                    raise Exception('Problem instance must be specified if using Random-Generated-Problems (else set num_random_inst = 0')
                elif (len(problem) > 1):
                    instances = problem[1]
                    if instances and not isinstance(problem[1], list):
                        instances = [instances]
                    if instances:
                        instances = domains_utils.lsof_domains.getDomain(kwargs['domain']).getInstances(instances)

                    # using randomly generated instances
                    if exp_settings.num_random_inst > 0 or exp_settings.random_reps:
                        if domains_utils.lsof_domains.getDomain(kwargs['domain'], 'rpg_folder') is None:
                            exp_utils.print_msg(kwargs['verbose_msg'], 'WARNING: '+kwargs['domain']+' does not have rpg_folder')
                        elif any(instance_is_rpg(instances)):
                            exp_utils.print_msg(kwargs['verbose_msg'], 'WARNING: At least one problem instance is RPG, do not have randomized instances of RPGs')
                            use_random_problem = False
                        else:
                            use_random_problem = True
                    if not use_random_problem:
                        # write instances as a string delimited by spaces
                        kwargs['problem'] = exp_utils.list2string(instances, sort = False, linebreak = False, delimiter = ' ')     # this will be written to .cfg

            # set the initial domain which will be used by planner (handled in .cpp)
            # the true domain .rddl is still copied to the working folder for rddlsim
            if initial_domain != 'true' and initial_domain:
                if '/' not in initial_domain:                                                                                      # not a path
                    kwargs['initial_domain'] = domains_utils.lsof_domains.getDomain(kwargs['domain'], initial_domain)
                    if kwargs['initial_domain'] is None:
                        exp_utils.print_msg(kwargs['verbose_msg'], 'ERROR: Domain ' + kwargs['domain'] + ' does not have ' + initial_domain + ' domain specified in domains_utils.py')
                        continue
                elif os.path.isfile(initial_domain):
                    kwargs['initial_domain'] = initial_domain
                else:
                    exp_utils.print_msg(kwargs['verbose_msg'], 'ERROR: Domain ' + kwargs['domain'] + ' does not have domain file ' + initial_domain)
                    continue
                if initial_domain != 'empty':
                    exp_utils.print_msg(kwargs['verbose_msg'], 'Model learner do not need to write preconditions if true preconditions are known in initial domain --> rddl_write_precondition = false')
                    kwargs['rddl_write_precondition'] = False
                else:
                    kwargs['rddl_write_precondition'] = True
            else:
                use_latent_model = True
                try:
                    use_latent_model = exp_settings.use_latent_model
                except AttributeError:
                    pass
                if use_latent_model:
                    latent_domain = domains_utils.lsof_domains.getDomain(kwargs['domain'], 'latent')
                    if latent_domain is not None:
                        kwargs['initial_domain'] = latent_domain
                        kwargs['prune'] = False
                        exp_utils.print_msg(kwargs['verbose_msg'], 'Domain ' + kwargs['domain'] + ' has latent domain specified in domains_utils.py, use it instead of true model')

            # set learners
            kwargs['planner'] = planner
            lff_is_applicable = True
            if kwargs.get('use_model_for_app_actions', True) and (initial_domain is None or initial_domain == 'true'):                                                                 # using true model so no executions will fail
                lff_is_applicable = kwargs['domain'] == 'triangle_tireworld' or kwargs['domain'] == 'turtlebot_survey'             # domains with deadends
            if isinstance(learners, str):
                learners = [learners]
            kwargs['learn_from_failure'] = False
            if lff_is_applicable:
                if 'lff-fo-bp' in learners or 'lff-bp-fo' in learners:
                    kwargs['learn_from_failure'] = True
                    kwargs['backpropagate_failure'] = True
                    kwargs['use_first_order_failure'] = True
                elif 'lff-bp' in learners:
                    kwargs['learn_from_failure'] = True
                    kwargs['backpropagate_failure'] = True
                elif 'lff-fo' in learners:
                    kwargs['learn_from_failure'] = True
                    kwargs['use_first_order_failure'] = True
                elif 'lff' in learners:
                    kwargs['learn_from_failure'] = True
            kwargs['learner'] = ''
            for l in exp_utils.options['learners']:
                if l in learners:
                    kwargs['learner'] = l
                    break

            kwargs['policy'] = policy
            kwargs['intrinsic_reward_types'] = intrinsic_reward_types
            kwargs['experience'] = exp
            kwargs['model_representation'] = model
            kwargs['beam_search_branch'] = 1
            if 'num_hypothesis_domains' not in kwargs:
                kwargs['num_hypothesis_domains'] = 1
            if plan_rollout:
                if plan_rollout[0]:
                    kwargs['multi_planning'] = plan_rollout[0]
                if plan_rollout[1]:
                    kwargs['beam_search_branch'] = plan_rollout[1]
                if plan_rollout[2]:
                     kwargs['num_hypothesis_domains'] = plan_rollout[2]
                if plan_rollout[3]:
                    kwargs['plan_rollout_horizon'] = plan_rollout[3]
            
            # temporarily set the value for kwargs['problem'] as interpret_function_approximation needs it, this will be initialized later on
            kwargs['given_order_key'] = problem
            kwargs = interpret_function_approximation(fa, **kwargs)                                             # can only call this after kwargs['problem'] is defined
            kwargs = check_settings(**kwargs)                                                                   # check if settings are correct

            # get list of files to import
            import_transitions_filenames, import_qvalue_filenames, import_rddl_filenames, import_tabu_filenames, import_intrinsic_filenames = \
                get_imported_files(['transition', 'policy', 'domain', 'tabu', 'intrinsic'], **kwargs)

            # must be done after check_settings: setup import/export of files to accumulate knowledge (Q-values, transitions) acquired thus far
            kwargs['imported_files'] = []
            if not import_tabu_filenames and kwargs.get('tabu_file', None):
                filename = kwargs['tabu_file'].replace('*', kwargs.get('domain', ''))
                if os.path.isfile(filename):
                    kwargs['imported_files'].append(filename)                                                   # file will be copied to logfolder
                    kwargs['tabu_file'] = filename[filename.rfind('/')+1:]                                      # overwrite config to use copied file at logfolder
                # else:
                #     generalised_tabu_file = kwargs['tabu_file'][:kwargs['tabu_file'].rfind('.')]+'_generalized'+kwargs['tabu_file'][kwargs['tabu_file'].rfind('.'):]
                #     if os.path.isfile(generalised_tabu_file):
                #         kwargs['imported_files'].append(generalised_tabu_file)

            if not import_transitions_filenames and kwargs.get('import_transition_file', None):                 # if using import_transitions_filenames (import a different file for each run), then don't accumulate transitions
                filename = kwargs['import_transition_file'].replace('*', kwargs.get('domain', ''))
                if os.path.isfile(filename):
                    kwargs['imported_files'].append(filename)                                                   # file will be copied to logfolder
                    kwargs['import_transition_file'] = filename[filename.rfind('/')+1:]                         # overwrite config to use copied file at logfolder
            
            if not import_rddl_filenames and kwargs.get('import_rddl_file', None):                              # if using import_rddl_filenames (import a different file for each run)
                if ' ' in kwargs['import_rddl_file']:
                    kwargs['import_rddl_file'] = [f.strip() for f in kwargs['import_rddl_file'].split(' ')]
                if isinstance(kwargs['import_rddl_file'], list):
                    files = []
                    for file in kwargs['import_rddl_file']:
                        if os.path.isfile(file):
                            # file may have same filename but different paths, so need to rename them since they will be copied to the same folder
                            filename = file[file.rfind('/')+1:]
                            filename = filename[: filename.rfind('.')] + '_' + str(len(files)) + filename[filename.rfind('.') :]
                            files.append(filename)
                            kwargs['imported_files'].append((file, filename))                                   # (file to be copied, new filename)
                    kwargs['import_rddl_file'] =  exp_utils.list2string(files, sort = False, linebreak = False, delimiter = ' ')
                else:
                    if os.path.isfile(kwargs['import_rddl_file']):
                        kwargs['imported_files'].append(kwargs['import_rddl_file'])
                        kwargs['import_rddl_file'] = kwargs['import_rddl_file'][kwargs['import_rddl_file'].rfind('/')+1:]
            
            if kwargs.get('import_qvalue', None):
                # if kwargs.get('lfa_use_non_fluents', 0) > 0:
                #     kwargs['lfa_use_non_fluents'] = 2
                #     exp_utils.print_msg(kwargs['verbose_msg'], 'If importing Q-function and using non-fluents, need to use every non-fluent as base features --> lfa_use_non_fluents = 2')
                filename = kwargs['import_qvalue'].replace('*', kwargs.get('domain', ''))
                if os.path.isfile(filename):
                    kwargs['imported_files'].append(filename)                                                   # file will be copied to logfolder
                    
                    # copy dual Q-function
                    dual_qvalue_filename = filename
                    dual_qvalue_filename = dual_qvalue_filename[: dual_qvalue_filename.rfind('.')] + '_dual' + dual_qvalue_filename[dual_qvalue_filename.rfind('.') :]
                    if os.path.isfile(dual_qvalue_filename):
                        kwargs['imported_files'].append(dual_qvalue_filename)
                    
                    # copy intrinsic reward Q-function
                    intrinsic_reward_filename = filename
                    intrinsic_reward_filename = intrinsic_reward_filename[: intrinsic_reward_filename.rfind('.')] + '_intrinsic' + intrinsic_reward_filename[intrinsic_reward_filename.rfind('.') :]
                    if os.path.isfile(intrinsic_reward_filename):
                        kwargs['imported_files'].append(intrinsic_reward_filename)

                    # overwrite config to use copied file at logfolder
                    kwargs['import_qvalue'] = filename[filename.rfind('/')+1:]

            if kwargs.get('import_intrinsic_reward', None):
                if os.path.isfile(kwargs['import_intrinsic_reward']):
                    kwargs['imported_files'].append(kwargs['import_intrinsic_reward'])                          # file will be copied to logfolder
                    kwargs['import_intrinsic_reward'] = kwargs['import_intrinsic_reward'][kwargs['import_intrinsic_reward'].rfind('/')+1:]    # overwrite config to use copied file at logfolder

            if kwargs.get('timed_constraints', None):
                if os.path.isfile(kwargs['timed_constraints']):
                    kwargs['imported_files'].append(kwargs['timed_constraints'])
                    kwargs['timed_constraints'] = kwargs['timed_constraints'][kwargs['timed_constraints'].rfind('/')+1:]
            
            kwargs = set_generated_files(**kwargs)                                                              # set the files to be copied after experiment is completed
            original_size = len(kwargs['imported_files'])

            # using randomly generated instances
            rpg_instances_for_each_rep = []
            if use_random_problem:
                # read folder where RPG instances are at, get list of randomly generated instances names
                rpg_folder = domains_utils.lsof_domains.getDomain(kwargs['domain'], 'rpg_folder')
                if rpg_folder is None:
                    raise Exception(kwargs['domain']+' does not have rpg_folder')
                if exp_settings.num_random_inst > 0:
                    num_random_inst = exp_settings.num_random_inst
                else:
                    num_random_inst = 1
                rpg_instances = rpg.getInstances(rpg_folder, instances)
                for r in rpg_instances:
                    r.sort(key=get_instance_index)
                for i in range(exp_settings.num_reps):
                    if True and num_random_inst == 1:                                                           # use lexical order of instances which is the same for each repetition
                        i = i + kwargs['seed'] - 1
                        selected_rpg_instances = []
                        for random_instances, instance in zip(rpg_instances, instances):
                            if random_instances == []:
                                exp_utils.print_msg(kwargs['verbose_msg'], 'WARNING: Problem instance "' + instance + '" does not have RPG problems')
                                selected_rpg_instances += [instance]
                            else:
                                if i >= len(random_instances):
                                    i_wrap = i - len(random_instances)
                                else:
                                    i_wrap = i
                                selected_rpg_instances += [random_instances[i_wrap]]
                    else:                                                                                       # RPE (this will generate a random sequence of instances for each repetition)
                        # select #num_random_inst randomly generated instances of each instance in instances (if problem has multiple instances)
                        selected_rpg_instances = []
                        repeat_count = 0
                        while True:
                            for random_instances, instance in zip(rpg_instances, instances):
                                if len(random_instances) == 0:
                                    raise Exception('No RPG instances found in ' + rpg_folder + ' for instance ' + instance + ' (domain does not have RPG or instance is already RPG)')
                                # replicate vector of rpg instances if there are insufficent rpg instances
                                duplicate_factor = math.ceil(num_random_inst / len(random_instances))
                                if exp_settings.rpg_seed:
                                    random.seed(exp_settings.rpg_seed+repeat_count)
                                else:
                                    random.seed(kwargs['seed']+i+repeat_count)
                                selected_rpg_instances += random.sample(random_instances*duplicate_factor, num_random_inst)
                            if selected_rpg_instances in rpg_instances_for_each_rep and repeat_count < 20:
                                # this combination of RPG instances have been added in a previous repetition, generate another combination by incrementing the random seed
                                repeat_count += 1
                                selected_rpg_instances = []
                            else:
                                break
                    # print(selected_rpg_instances)
                    rpg_instances_for_each_rep.append(selected_rpg_instances)

            # run client for #num_reps times
            for rep_count in range(exp_settings.num_reps):
                if rep_count in skip_repetitions:                        # skip this repetition count, this is useful for continuing a set of experiments
                    kwargs['seed'] += 1
                    continue
                # using randomly generated instances
                if use_random_problem:
                    # write instances as a string delimited by spaces, this will be written to .cfg
                    kwargs['problem'] = exp_utils.list2string(rpg_instances_for_each_rep[rep_count], sort = False, linebreak = False, delimiter = ' ')
                # kwargs = interpret_function_approximation(fa, **kwargs)             # can only call this after kwargs['problem'] is defined

                # if importing a different transition training file for each repetition
                if import_transitions_filenames:
                    kwargs['imported_files'].append(import_transitions_filenames[rep_count])

                if import_rddl_filenames:
                    if isinstance(import_rddl_filenames[rep_count], list):
                        files = []
                        for file in import_rddl_filenames[rep_count]: 
                            # file may have same filename but different paths, so need to rename them since they will be copied to the same folder
                            filename = file[file.rfind('/')+1:]
                            filename = filename[: filename.rfind('.')] + '_' + str(len(files)) + filename[filename.rfind('.') :]
                            files.append(filename)
                            kwargs['imported_files'].append((file, filename))                                   # (file to be copied, new filename)
                        kwargs['import_rddl_file'] =  exp_utils.list2string(files, sort = False, linebreak = False, delimiter = ' ')
                    else:
                        kwargs['imported_files'].append(import_rddl_filenames[rep_count])                       # import_rddl_filenames[rep_count] might be a list, do not use += as we want to delete the entire entry later on
                
                if import_qvalue_filenames:
                    if exp_settings.urgent and kwargs['seed']-1 < len(import_qvalue_filenames):
                        qvalue_filename = import_qvalue_filenames[kwargs['seed']-1]                             # if using 'urgent' way of running experiments
                    else:
                        qvalue_filename = import_qvalue_filenames[rep_count]
                    dual_qvalue_filename = qvalue_filename[: qvalue_filename.rfind('.')] + '_dual' + qvalue_filename[qvalue_filename.rfind('.') :]
                    intrinsic_reward_filename = qvalue_filename[: qvalue_filename.rfind('.')] + '_intrinsic' + qvalue_filename[qvalue_filename.rfind('.') :]
                    kwargs['imported_files'].append(qvalue_filename)
                    kwargs['imported_files'].append(dual_qvalue_filename)
                    kwargs['imported_files'].append(intrinsic_reward_filename)

                if import_tabu_filenames:
                    if exp_settings.urgent and kwargs['seed']-1 < len(import_tabu_filenames):
                        kwargs['imported_files'].append(import_tabu_filenames[kwargs['seed']-1])                 # if using 'urgent' way of running experiments
                    else:
                        kwargs['imported_files'].append(import_tabu_filenames[rep_count])
                
                if import_intrinsic_filenames:
                    if exp_settings.urgent and kwargs['seed']-1 < len(import_intrinsic_filenames):
                        kwargs['imported_files'].append(import_intrinsic_filenames[kwargs['seed']-1])            # if using 'urgent' way of running experiments
                    else:
                        kwargs['imported_files'].append(import_intrinsic_filenames[rep_count]) 
                

                if rep_count == 0:
                    short_desc, _ = exp_utils.get_summary_of_experiment(**kwargs)
                    if short_desc:
                        f = open(exp_utils.mbrrl_path + '/' + exp_utils.summary_file, 'a+')
                        f.write(short_desc+'\n')
                        f.close()

                status = exp_utils.run_client(**kwargs)                             # run client

                kwargs['imported_files'] = kwargs['imported_files'][: original_size]
                if status == 0:
                    sys.exit()
                if exp_settings.client_args.get('print_usage', False):
                    break
                kwargs['seed'] += 1

    elif runtime_args['-ops'] == 'server':
        server_args = {}
        server_args['port'] = runtime_args['-port']
        server_args['log_path'] = exp_utils.impt_paths['log_path'].replace('results', 'results-'+str(runtime_args['-port']))
        server_args['benchmark_dir'] = benchmark_dir
        server_args['num_rounds'] = exp_settings.num_rounds
        try:
            if exp_settings.urgent and exp_settings.num_reps == 1 and exp_settings.num_split_learning <= 1:
                server_args['ind_session'] = 1                                          # RDDLsim terminates after one session
            else:
                server_args['ind_session'] = 0                                          # RDDLsim will not terminate until manually terminated
        except:
            pass
        exp_utils.run_server(**server_args)
    elif runtime_args['-ops'] == 'finish':
        combinations =  create_experiments_combinations(fa_index)
        for problem, planner, learners, policy, exp, initial_domain, fa, plan_rollout in combinations:
            if policy is None:
                save_folder = 'experiment_' + problem + '_' + planner
            else:
                save_folder = 'experiment_' + problem + '_' + planner + '_' + policy
            template_files_ = [problem+'_'+file for file in exp_utils.template_files]
            exp_utils.finish_experiment(save_folder, exp_utils.generated_files, template_files_)
    else:
        raise Exception('./run_experiments.py [name of experiment settings] [client or server or help] <port_num>')