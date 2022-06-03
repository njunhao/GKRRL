#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:58:30 2019

@author: alvin
"""

import os
import subprocess
import shutil
import copy
import glob
import sys
import operator
import time
from datetime import datetime

DISABLE_LIBNOTIFY=True
# try:
    # from gi.repository import Notify
    # DISABLE_LIBNOTIFY=False
# except ImportError:
#     DISABLE_LIBNOTIFY=True

if os.getcwd().find(os.sep+'mbrrl'+os.sep) >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find(os.sep+'mbrrl'+os.sep)+len(os.sep+'mbrrl'+os.sep)]
elif os.getcwd().find(os.sep+'mbrrl') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find(os.sep+'mbrrl')+len(os.sep+'mbrrl')]
else:
    raise Exception("Unable to determine library path, current directory is " + os.getcwd())
working_path = mbrrl_path
# set directory for writing files to during experiment, set to /scratch if running batch experiments on a server



# ----- SETTINGS ----- #
binary_file = 'mbrrl'
logfile = 'mbrrl_console.log'
summary_file = 'summary.log'
opennn_training_file = 'training_data.dat'
ros_path = os.path.join(mbrrl_path, '..', '..', 'ROS', 'ROSPlan', 'src', 'rosplan', 'rosplan_rl', 'common')
generated_files = {
        'log': [logfile, 'mbrrl.log', 'intrinsic_reward.dat', 'ruleslearner.log', 'action_duration.log', 'learned_domain.rddl'],
        'ros': [ros_path+'ros_console.log', ros_path+'ros.bag'],
        'optional': ['transitions_all.dat'],
        'opennn': [opennn_training_file, 'data_set.xml', 'neural_network.xml', 'expression.txt', 'training_strategy.xml', 'training_strategy_results.dat'],
        'pattern': ['learned_domain_*.rddl', 'learned_domain_*.ppddl', '*_intrinsic.dat', 'error_*', 'debug_*', 'analysis_*', 'replay_*', '*_progress_*.log'],
        'pattern_optional': ['lfit_rules_*.dat', 'transitions_*.dat', 'parser_in_*', 'parser_out_*', 'UCT_search_*'] #, 'prost_search_*']
}

# exclude these from generated_files_pattern: 'learned_domain_inst_*.txt'
template_files = ['mdp_template.pddl', 'inst_mdp_template.pddl', 'config.cfg', 'known_mappings.dat'];

# remove these files after experiment
tmp_files = ['learned_domain_inst.txt', 'transitions_tmp.dat']

impt_paths = {
        'log_path': os.path.join(working_path, 'results', 'current'),
        'features_path': os.path.join(mbrrl_path, 'domains', 'robots_features')
}

generic_files = {
        'bin_debug': os.path.join(mbrrl_path, 'build', 'src', binary_file),
        'bin_release': os.path.join(mbrrl_path, 'src', binary_file),
        'rddl_parser': os.path.join(mbrrl_path, 'external', 'prost', 'rddl-parser-release'),
        'noprune_rddl_parser': os.path.join(mbrrl_path, 'external', 'prost', 'simple-rddl-parser'),
        'log_conf': os.path.join(mbrrl_path, 'scripts', 'run_experiments', 'logger.conf'),
        'learner_conf': os.path.join(mbrrl_path, 'scripts', 'run_experiments', 'ruleslearner_logger.conf'),
        'run-server': os.path.join(mbrrl_path, 'scripts', 'run_experiments' ,'run-server')
}

# goal sequence if using given-ordered-context, this will be set in run_experiments.py
lfa_goal_sequence = {
        ('grid_survey', 1): "object_found(o2); object_found(o3); object_found(o4); object_found(o5)",
        ('grid_survey', 2): "object_found(o2); object_found(o3); object_found(o4); object_found(o5)",
        ('grid_survey', 'b1'): "object_found(o1); object_found(o2); object_found(o4); object_found(o5)",
        ('grid_survey', 'b2'): "object_found(o1); object_found(o3); object_found(o9); object_found(o11)",
        ('grid_survey', 'sq3'): "object_found(o1); object_found(o3); object_found(o7); object_found(o9)",
        ('grid_survey', 'sq4'): "object_found(o1); object_found(o4); object_found(o13); object_found(o16)",
        ('grid_survey', 'sq5'): "object_found(o1); object_found(o5); object_found(o21); object_found(o25)",
        ('robot_inspection', 3): "object_info_received(o4); object_info_received(o3); object_info_received(o2); object_info_received(o0); object_info_received(o1)",
        ('robot_inspection', 5): "object_info_received(o0); object_info_received(o4); object_info_received(o3); object_info_received(o2); object_info_received(o5); object_info_received(o1)",
        ('academic_advising', 3): "passed(CS12); passed(CS13); passed(CS31); passed(CS41);",
        ('academic_advising', 5): "passed(CS12); passed(CS14); passed(CS21); passed(CS33); passed(CS34); passed(CS43); passed(CS42); passed(CS53);",
        ('recon2', 3): "pictureTaken(o2); pictureTaken(o1); pictureTaken(o3); pictureTaken(o4); pictureTaken(o0);",
        ('recon2', 6): "pictureTaken(o0); pictureTaken(o3); pictureTaken(o5); pictureTaken(o4); pictureTaken(o2);  pictureTaken(o1);",
        ('recon2', '0e'): "pictureTaken(o0); pictureTaken(o1); pictureTaken(o2);",
        ('recon2', '3e'): "pictureTaken(o2); pictureTaken(o1); pictureTaken(o3); pictureTaken(o4); pictureTaken(o0);",
        ('recon2', '6e'): "pictureTaken(o0); pictureTaken(o3); pictureTaken(o5); pictureTaken(o4); pictureTaken(o2);  pictureTaken(o1);",
        ('recon2', 9): "pictureTaken(o1); pictureTaken(o4); pictureTaken(o6); pictureTaken(o0); pictureTaken(o3);  pictureTaken(o5); pictureTaken(o2);",
        ('grid_survey', 'sq5'): "object_found(o1); object_found(o21); object_found(o25); object_found(o5);"
}

alias = {
        'prost': ['prost'],
        'uct': ['uct'],
        'vi': ['vi', 'valueiteration', 'value iteration', 'value_iteration'],
        'pi': ['pi', 'policyiteration', 'policy iteration', 'policy_iteration'],
        'qlearning': ['qlearning', 'q learning'],
        'doubleq': ['doubleq', 'doubleqlearning', 'double q learning', 'double qlearning'],
        'dual-doubleq': ['dual-doubleq', 'ddoubleq'],
        'ql': ['ql', 'q lambda'],
        'sarsa': ['sarsa'],
        'sarsal': ['sarsal', 'sarsa l', 'sarsa lambda'],
        'rmax': ['rmax', 'r max', 'r-max'],
        'vmax': ['vmax', 'v max', 'v-max'],
        'dynaq': ['dynaq', 'dyna-q'],
        'dyna2': ['dyna2', 'dyna 2'],
        'ps': ['prioritizedsweeping', 'ps'],
        'epsilon': ['epsilon', 'eps'],
        'softmax': ['softmax'],
        'thompson': ['thompson', 'ts', 'thompson_sampling'],
        'thompson-ucb': ['thompson-ucb', 'tsu', 'thompson_sampling_ucb'],
        'ucb': ['ucb']
}
all_alias = []
for key, values in alias.items():
    all_alias += values

def_server_args = {
        'home_dir': os.path.join(mbrrl_path, 'external', 'prost', 'testbed'),   # this is not used if nargs > 1
        'benchmark_dir': os.path.join(mbrrl_path, 'domains', 'experiments'),    # arg2: benchmark directory (required input)
        'port': 2323,                                                           # arg3: portnumber
        'num_rounds': 5,                                                        # arg4: number of rounds
        'seed': 1,                                                              # arg5: random seed
        'ind_session': 0,                                                       # arg6: individual session (0/1 for false/true)
        'timeout': 0,                                                           # arg7: use timeout (0/1 for false/true)
        'log_path': impt_paths['log_path'],                                     # arg8: log folder
        'monitor_exec': 1                                                       # arg9: monitor execution (0/1 for false/true)
}

# order of arg given to shell script
server_args_order = ['home_dir', 'benchmark_dir', 'port', 'num_rounds', 'seed', 'ind_session', 'timeout', 'log_path', 'monitor_exec']

# most of the options are deprecated as we use config.cfg to pass in parameters instead
# tuple: (type, default value)
# if type starts with -- then this is to pass in as arguments when calling mbrrl binary as optional arguments
# if type is numeric, then this is to pass in as non-optional arguments with the # indicating the position of the argument when calling mbrrl binary
# if type is 'config', then this is used to overwrite .cfg config_file that is used for experiments, the key must match the parameter name in .cfg
# if type is None, then this is not passed to CPP in any way
def_client_args = {
        # ---------- Misc
        'log_path': (1, impt_paths['log_path']),
        'config_file': (2, os.path.join(impt_paths['log_path'], 'config.cfg')),
        'save_file': ('config', True),                              # Save files generated in each round
        'log_conf': ('config', generic_files['log_conf']),
        'learner_conf': ('config', generic_files['learner_conf']),
        'simulator_host': ('config', 'localhost'),
        'simulator_port': ('config', def_server_args['port']),
        'rddl_parser': ('config', generic_files['rddl_parser']),
        'reward_step_forward': ('config', None),                    # True if domain has immediate rewards which are feedback from simulator 1 step later (False if using ROS)
        'timed_constraints': ('config', None),                      # folder for file timed_constraints_*.txt (* is problem instance number) which specifices timed constraints
                                                                    # Format "start_time: (action_or_state_fluent_name arg1 arg2)  [duration]", if start_time < 0, then this is a dynamic goal
                                                                    # Format "Max Makespan = 1000" where 1000 is the max mission time in seconds
        'allow_latent_objects': ('config', None),                   # If true and problem has latent objects, discover latent objects online
        'dynamic_constraint_duration': ('config', None),            # If > 0 and problem has dynamic goals, then dynamic goals are considered as dynamic time constrained goals with end time constraint = start time + dynamic_constraint_duration

        # ---------- Verbose
        # 'verbose_step': ('--verbose_step', True),                 # example of passing in argument
        'verbose_state': ('config', 1),                             # 0: no print, 1: print state vector, [2]: print true state fluents, 3: print all state fluents
        'verbose_action': ('config', 1),                            # 0: no print, [1]: print Q-values of applicable actions, 2: print Q-values for model-based and model-free
        'verbose_step': ('config', 1),                              # 0: no print, [1]: print applicable actions / policy / Q-function step-update, 2: print details of applicable actions / policy, and 3: print 
        'verbose_search': ('config', 0),                            # 0: no print, [1]: print PROST search / MQTE result / UCT / rollout / self-play, 2: print MQTE/UCT search tree / details of self-play, 3: print more details of UCT search tree
        'verbose_analysis': ('config', 0),                          # 0: no print, [1]: print analysis (ordered goals, context, SIGMA, TD error), 2: print details, 3: print more details
        'verbose_hyothesis_model': ('config', 1),                   # 0: no print, 1: print details for multi-hypothesis model planning
        'verbose_debug': ('config', 0),                             # 0: no print, 1: print goal context for each action, 2: print active features, [3]: print active first-order features and their grounding, 4:
        
        # ---------- Training Data
        'all_transitions_file': ('config', None),                   # transition file to export to
        'import_transition_file': ('config', None),                 # transition file to import from
        'import_transition_folder': (None, None),                   # location of root folder where folders containing transitions files are at
        'import_transitions_num': ('config', None),                 # Number of transitions to import (if None then imports all)
        'import_transition_reset': ('config', None),                # If true, delete imported transitions at start of first round
        'import_knowledge_folder': (None, None),                    # location of root folder where folders containing import_qvalue file, tabu_file file, or/and import_intrinsic_reward files are at (* will be replaced by domain name)

        # ---------- Model
        'initial_domain': ('config', None),
        'use_model_for_app_actions': ('config', False),             # set to True to use model to determine if action is applicable
        'use_model_for_prediction': ('config', False),              # set to True to use model to predict s', r (required for self-play and pruning useless actions)
        'evaluate_model_prediction_error': ('config', False),       # evaluate model prediction error
        'mve_horizon': ('config', None),                            # MVE horizon
        'mqte_horizon': ('config', None),                           # MQTE horizon (set to -X to use MQTE all the time with horizon X)
        'noop_actions_allowed': ('config', None),                   # set to True to allow NOOP actions to be selected (it will still be selected if its the only option)
        'sync_model': ('config', True),                             # if true, transition & reward matrices are constructed for every element, can be slow for large domains
        'record_transitions': ('config', False),                    # If true, record transitions
        'always_update_q': ('config', True),                        # if true, update Q-values even if action fail to execute
        'experience': ('config', 'list'),                           # matrix, list, relational (matrix exploiting relational structure)
        'model_representation': ('config', 'list'),                 # matrix, list, or dbn
        'import_multi_rddl': (None, None),                          # number of RDDL models to import (for multi-model planning)
        'import_rddl_file': ('config', None),                       # RDDL file to import
        'import_rddl_folder': (None, None),                         # location of root folder where folders containing RDDL files are at
        'fix_rddl_domain': ('config', False),                       # If true, augment CPF from input RDDL domain file with remaining information from true RDDL domain file

        # ---------- Loop Detection
        'max_loop_size': ('config', 0),                             # Max. size of loop to detect
        'prune_useless_action': ('config', False),                  # If true, prune useless actions

        # ---------- Planning
        'multi_planning': ('config', None),                         # Planning strategy when there are multiple hypothesis models: best, common, or safe
        'self_play_horizon': ('config', None),                      # no. of steps to do self-play to initialize Q-values
        'self_play_repetitions': ('config', None),                  # no. of repetitions for self-play
        'plan_rollout_horizon': ('config', None),                   # no. of steps to rollout simulated plan
        'plan_rollout_max_attempt': ('config', None),               # No. of attempts to try plan rollout if it fails
        
        # ---------- Temporal Reasoning
        'max_action_duration': ('config', None),                    # Maximium duration expected (seconds) which is used to normalize action cost, set to 0 to exclude duration as cost

        # ---------- Learners
        'learning': ('config', None),
        'learner': ('config', None),                                # Model learning algorithm
        'features_learner': ('config', None),                       # Features learning algorithm
        'rddl_write_precondition': ('config', None),                # If true, model learner writes precondition to .rddl
        'learner_timeout': ('config', 500),                         # Timeout in seconds for model learner
        'learn_from_failure': ('config', None),                     # If true, learn from failures and deadends
        'use_first_order_failure': ('config', None),                # Learn from failure with first-order state features
        'backpropagate_failure': ('config', None),                  # Backpropagate failure when learning from failure
        'tabu_file': ('config', None),                              # Import/export TABU from this file
        'learner_output_file': ('config', None),                    # Logfile for rules learner output
        'learning_step_size': ('config', 1),                        # Learn a model after the accumulated number of transitions for an action since the last learning took place equals this number
        'max_round_for_learning': ('config', None),                 # Perform model learning up till this number of rounds
        'max_transitions_per_action': ('config', 100),              # Max num of training data per action
        'beam_search_branch': ('config', 1),                        # Branching factor for beam search in rules learner
        'num_hypothesis_domains': ('config', 0),                    # no. of hypothesis RDDL models to consider in planning
        'evaluate_model_req_num_sf': ('config', None),              # Min. number of state fluents with non-trivial CPFs to consider model is good
        'evaluate_model_req_num_af': ('config', None),              # Min. number of actions to appear in CPFs to consider model is good

        # ---------- Local Minimum Detection
        'use_local_min_detection': ('config', False),               # Set to true to detect local minimum and wipe slate clean
        'local_min_avg_visit_threshold': ('config', None),          # If average number of visits for each state exceeds this number, then policy is looping
        'local_min_no_goal_threshold': ('config', None),            # If number of successive rounds where goal is not reached exceeds this threshold, then local minimum is likely
        'local_min_stationary_policy_threshold': ('config', None),  # If number of successive rounds where policy is unchanged, then policy might be stationary
        'local_min_non_goal_penalty': ('config', None),             # Reward for not reaching goal at end of episode
        
        # ---------- Intrinsic Reward
        'intrinsic_reward_types': ('config', None),                 # select intrinsic reward model (can have more than one)
        'intrinsic_reward_coefficent': ('config', None),            # Coefficient for intrinsic reward: r = r_extrinsic + coeff * r_intrinsic
        'intrinsic_reward_coefficent_decay': ('config', None),      # Decay factor for coefficient for intrinsic reward
        'intrinsic_reward_aggregation': ('config', None),           # Aggregation method for multiple types of intrinsic reward: average, max, or sum
        'reward_for_failed_execution': ('config', None),            # reward for failed execution

        # ---------- Function Approximation
        'online_q_update': ('config', None),                        # If true, update Q-values online. Otherwise, only update at the start if training data is provided, Q-values are imported, or performing self-play
        'function_approximation': ('config', 'linear'),             # exact = tabular, linear = linear FA
        'lfa_norm_reward': ('config', None),                        # normalization reward for LFA
        'lfa_base_features': ('config', None),                      # schema to get base (initial) features
        'lfa_common_learning': ('config', False),                   # If a feature is learned for an action, add the feature to remaining actions
        'lfa_first_order_features': ('config', False),              # If true, use first-order features
        'lfa_asymmetric_update': ('config', False),                 # If true, use asymmetric update (only applicable if using MBFS)")
        'lfa_aggressive_pruning': ('config', False),                # If true, prune features by lifted generalization followed by features grounding
        'lfa_use_non_fluents': ('config', 0),                       # If == 1, include selective non-fluents in features, if == 2, include every non-fluent
        'lfa_use_neg_features': ('config', False),                  # If true, include negation of fluents in features
        'lfa_use_decoupled_weights': ('config', False),             # If true, each action of the same lifted action will have separate weights (only applicable if using first-order features)
        'lfa_free_var_substitution': ('config', ''),                # maximization criteria for substituting existential parameters: 'qvalue', 'state', 'abs', or 'specific'
        'lfa_conflict_resolution_level': ('config', None),          # Conflict resolution level between ground context and goal context if ground context takes precedence
        'lfa_max_num_free_var': ('config', 2),                      # max num. of free variables allowed in a first-order feature
        'lfa_batch_retrain': ('config', False),                     # If true, reset weights and relevance and replay at end of episode if new features are added during the episode
        'lfa_goal_sequence': ('config', None),                      # Sequence of goal fluents to be used for ordered goal context
        'lfa_mbfs_parameters': ('config', None),                    # Parameters for MBFS, strings of 1's and 0's to represent true/false, respectively ("include_precond", "include_precond_of_reward", "include_reward", "exclude_noop_arc", "include_coparents_of_state_fluent", "include_ancestors_of_state_fluent", "include_neighbours_of_ancestors_of_state_fluent", "include_coparents_of_immediate_child_fluent", "include_coparents_of_action")
        'lfa_import_weights': ('config', None),                     # If importing LFA, besides importing features, also import weights if this is true
        'eligibility_trace_type': ('config', 'replacing'),          # Eligibility type (accumulating, replacing, or dutch)
        'allow_trivial_eligibility_update': ('config', True),       # If true, always perform n-step update, else do not perform if transition is trivial (i.e., s = s1 and reward = action cost)
        'reset_eligibility_trace_per_subgoal': ('config', False),   # If true, reset eligibility traces when a subgoal is achieved
        'ifdd_discovery_threshold': ('config', 3.0),                # iFDD parameter: discovery threshold
        'ifdd_max_feature_size': ('config', 2),                     # iFDD parameter: maximum number of fluents allowed per feature
        'ifdd_initial_feature_size': ('config', 0),                 # iFDD parameter: maximum number of fluents allowed per feature which is added at the start
        'ifdd_batch_size': ('config', 0),                           # iFDD parameter: batch learning size, set > 1 if using Batch-iFDD
        'ifdd_max_features_addition': ('config', 1),                # iFDD parameter: maximum number of features to add greedily per batch learning
        'revert_to_best_policy': ('config', False),                 # Revert to best previous policy if current policy deteriorates
        'replay_trajectory_to_goal': ('config', False),             # Replay observed trajectories reaching goals at end of episode for goals which are not achieved
        'max_replay_buffer': ('config', None),                      # Maximum number of most recent transitions for replay

        # ---------- Neural Network
        'training_data_file': ('config', opennn_training_file),
        'training_ratio': ('config', 0.6),                          # Percentage of training data used for training
        'selection_ratio': ('config', 0.2),                         # Percentage of training data used for selection
        'testing_ratio': ('config', 0.2),                           # Percentage of training data used for testing
        'hidden_perceptrons_number': ('config', 9),                 # Number of neurons in hidden layer
        'max_epochs_number': ('config', 100),                       # Maximum no. of epoch for training
        'display_period': ('config', 10),                           # Number of epochs between the training showing progress
        'min_loss_decrease': ('config', 1.0e-6),                    # Minimum improvement in the loss between two epochs
        'min_parameters_increment_norm': ('config', 0.0),           # Minimum parameters increment norm stopping criterion
        'update_size': ('config', 10)                               # Update once per update_size
}

# tuple: (cmdline flag, default value, <list of algorithms this arg is applicable, omit if all are applicable>)
def_algo_args = {
        'seed': ('-s', 1),
        'searchengine': ('-se', '[IPPC2014]', alias['prost']),
        'alpha': ('-alpha', 0.1, alias['qlearning']+alias['doubleq']+alias['dual-doubleq']+alias['ql']+alias['sarsa']+alias['dynaq']+alias['dyna2']+alias['sarsal']),
        'discount': ('-discount', 1.0, alias['uct']+alias['rmax']+alias['vmax']+alias['qlearning']+alias['doubleq']+alias['dual-doubleq']+alias['ql']+alias['sarsa']+alias['dynaq']+alias['dyna2']+alias['sarsal']+alias['ps']),
        # 'lambda': ('-lambda', 0.1, alias['dyna2']+alias['sarsal']+alias['ql']),
        # 'tolerance': ('-tolerance', 0.001, alias['vi']+alias['pi']+alias['dyna2']+alias['sarsal']+alias['ql']),
        # lambda and tolerance is used in all model-free algorithms that uses LFA
        'lambda': ('-lambda', 0.1, alias['qlearning']+alias['doubleq']+alias['dual-doubleq']+alias['ql']+alias['sarsa']+alias['dynaq']+alias['dyna2']+alias['sarsal']+alias['ps']),
        'tolerance': ('-tolerance', 0.001, alias['vi']+alias['pi']+alias['qlearning']+alias['doubleq']+alias['dual-doubleq']+alias['ql']+alias['sarsa']+alias['dynaq']+alias['dyna2']+alias['sarsal']+alias['ps']),
        # 'rmax': ('-rmax', 1, alias['rmax']+alias['vmax']),                                # Deprecated, this is automatically set to norm_reward
        'visitation_threshold': ('-visitation_threshold', 3, all_alias),
        'batch': ('-batch', 0, alias['doubleq']+alias['dual-doubleq']),                     # If = 1, update target FA at the end of episode, else, randomly update a FA
        'dual': ('-dual', 0, alias['dual-doubleq']),                                        # = 1: use sum of FA as policy; = 0: consider GND FA as policy; if between 0 and 1: threshold for switching out of imported fixed policy (if applicable)
        'batch_size': ('-batch_size', 50, alias['dynaq']+alias['dyna2']+alias['ps']),
        'theta  ': ('-theta', 0.5, alias['ps']),                                            # Threshold for change in Value to add to priority queue
        'policy': ('-policy', 'thompson'),                                                  # Choice of policy
        'temp': ('-temp', 1.0, alias['softmax']),                                           # Softmax temp
        'fucb': ('-fucb', 1.0, alias['ucb'], alias['thompson-ucb']),                        # UCB coefficient
        'epsilon': ('-epsilon', 0.1, alias['epsilon']+alias['ql']+alias['uct']),            # Epsilon
        'decay': ('-decay', 0.1, all_alias),                                                # Rate at which epsilon/temp decrease at the end of each round, also controls coefficient for intrinsic reward
        'depth': ('-depth', 15, alias['rmax']+alias['vmax']+alias['prost']+alias['uct']),   # Maximum search depth, if < 0, then this is equal to planning horizon
        'timeout': ('-timeout', 10, alias['uct']),                                          # Maximum runtime (seconds)
        'max_iteration': ('-max_iteration', 0, alias['uct']),                               # Maximum number of iterations and maximum number of expanded nodes
        'rollout_horizon': ('-rollout_horizon', 10, alias['uct']),                          # Maximum simulation rollout horizon
        'policy_rollout_horizon': ('-policy_horizon', 0, alias['uct']),                     # Simulation rollout length using policy generated from Q-function instead of random policy
        'mixing_factor': ('-mixing', 0, alias['uct']),                                      # Mixing factor for leaf node: (1-mixing)*rollout value + mixing*Q(s,a)
        'reuse_tree': ('-reuse', 0, alias['uct']),                                          # If 1, then reuse search tree from previous episode
        'prune_actions': ('-prune_actions', 0, alias['uct']),                               # If 1, then prune useless actions
        'early_termination': ('-early_termination', 0, alias['uct']),                       # If 1, then terminate early if condition is satisfied
        'most_visited': ('-max_visit', 0, alias['uct']),                                    # If 1, then select most visited node rather than node with max value
        'deadend_reward': ('-deadend_reward', 0, alias['uct']),                             # If 1, then overwrite deadend reward
        'import_policy': ('-import_policy', None),                                          # Location of policy file
        'export_policy': ('-export_policy', None),                                          # Location of policy file
        'import_qvalue': ('-import_qvalue', None),                                          # Location of q value file
        'export_qvalue': ('-export_qvalue', None),                                          # Location of q value file
        'import_intrinsic_reward': ('-import_intrinsic_reward', None),                      # Location of intrinsic reward file
        'export_intrinsic_reward': ('-export_intrinsic_reward', None),                      # Location of intrinsic reward file
        'plans_file': ('-plans_file', None)                                                 # Absolute path of file
}

# for usage in run_experiments.py
options = {
    'planners': ['prost', 'uct', 'rmax', 'qlearning', 'doubleq', 'dual-doubleq', 'ql', 'sarsa', 'sarsal', 'dynaq', 'dyna2'], # deprecated: 'vmax', 'vi', 'pi', in progress: 'ps'
    'policies': ['greedy', 'ucb', 'epsilon', 'softmax', 'softmax-ucb', 'thompson', 'thompson-ucb', 'random', 'import'],
    'learners': ['lfit', 'pasula'],
    'features_learners': ['ifdd', 'ifdd+'],
    'experiences': ['list', 'relational'],                                  # 'matrix' is deprecated; list, relational (matrix exploiting relational structure)
    'model_representations': ['list', 'dbn'],                               # 'matrix' is deprecated
    'function_approximations': ['exact', 'neural_network', 'linear'],
    'lfa_base_features': ['all', 'param', 'cpf', 'import'],
    'lfa_substitutions_operator': ['or', 'sum'],
    'lfa_substitutions_metric': ['qvalue', 'state', 'abs', 'specific'],
    'lfa_substitutions_context': ['ground', 'location', 'goal', 'given', 'ordered', 'proximity', 'synergy'],
    'problems_ippc': ['academic_advising', 'crossing_traffic', 'elevators', 'game_of_life', 'navigation', 'recon', 'skill_teaching', 'sysadmin', 'tamarisk', 'triangle_tireworld', 'wildfire'],
    'problems_robot': ['grid_survey', 'husky_inspection', 'recon2', 'robot_inspection', 'taxi', 'tiago', 'tiago_fetch', 'turtlebot', 'turtlebot_goal', 'turtlebot_survey'],
    'initial_domains': ['empty', 'approx', 'true'],                         # may have more types, see domains_utils.py
    'multi_planning': [None, 'safe', 'best', 'common', 'semihybrid', 'hybrid', 'linear-semihybrid', 'linear-hybrid'],
    'intrinsic_reward_types': [None, "rmax", "visit_count", "model_learner", "td_error", "delta_td_error", "goal_trajectory", "dowham", "first_order_explore", "first_order_target"],
    'benchmark_dir': ['', os.path.join(mbrrl_path, 'domains', 'experiments')]
}
options['problems'] = options['problems_ippc'] + options['problems_robot'] 


# -----------------------------
# -----------------------------
# -----------------------------
#       RUN COMMANDS
# -----------------------------
# -----------------------------
# -----------------------------

def run_server(**kwargs):
    # override default values
    server_args = copy.deepcopy(def_server_args)
    server_args.update(kwargs)
    # check if symbolic link is working
    if not os.path.isdir(server_args['home_dir']):
        raise Exception('Symbolic link to PROST is broken: ' + server_args['home_dir'])
    if not os.path.isdir(os.path.join(server_args['home_dir'], 'rddlsim')):
        print('Symbolic link to rddlsim via PROST is broken: ' + os.path.join(server_args['home_dir'], 'rddlsim') + '  -  attempting to create symbolic link')
        os.symlink(os.path.join('..', '..', 'rddlsim'), os.path.join(server_args['home_dir'], 'rddlsim'))
    
    cmdline = '\"' + generic_files['run-server'] + '\"'
    for arg in server_args_order:
        if isinstance(server_args[arg], str) and os.sep in server_args[arg]:
            cmdline += ' \"' + str(server_args[arg]) + '\"'
        else:
            cmdline += ' ' + str(server_args[arg])
    print("Running on port " + str(server_args['port']))
    # subprocess.call('bash ' + os.path.join(server_args['home_dir'], 'rddlsim', 'compile'), shell=True)
    res = subprocess.call(cmdline, shell=True)
    if (res != 0):
        print('Unexpected error')
#        if not DISABLE_LIBNOTIFY:
#            Notify.init("MBRRL")
#            notify_msg = Notify.Notification.new("mbrrl","Unexpected error! ","dialog-error")
#            notify_msg.show ()
#        raise RuntimeError


def run_client(**kwargs):
    # initialize
    if not kwargs['prune']:
        kwargs['rddl_parser'] = generic_files['noprune_rddl_parser']
    else:
        kwargs['rddl_parser'] = generic_files['rddl_parser']
    kwargs['runtime_verbose_msg'] = []
    # domain = kwargs['problem']
    # can't rmb what these lines below are for
    # if kwargs['problem'].find("_") == -1:
    #     domain = kwargs['problem']
    # else:
    #     domain = kwargs['problem'][:kwargs['problem'].find("_")]
    kwargs['config_file'] = os.path.join(kwargs['log_path'], kwargs['domain']+'_config.cfg')
    
    # clear folder first
    if not os.path.exists(kwargs['log_path']):
        os.makedirs(kwargs['log_path'], exist_ok=True)
    else:
        remove_all_files_in_folder(kwargs['log_path'])

    # copy files
    template_files_ = [kwargs['domain']+'_'+file for file in template_files]
    while True:
        copy_files(template_files_, kwargs['benchmark_dir'], kwargs['log_path'], True)
        if not os.path.isfile(kwargs['config_file']):
            print('File has not been copied (have you ran the server?), trying again...')
            time.sleep(3)
        else:
            break
    
    for files in kwargs['imported_files']+[generic_files['log_conf'], generic_files['learner_conf']]:
        if not isinstance(files, list):
            files = [files]
        for file in files:
            try:
                if isinstance(file, tuple):     # tuple is (file to be copied, filename to be used for pasting)
                    shutil.copy2(file[0], os.path.join(kwargs['log_path'], file[1]))
                    if not kwargs.get('print_usage', False) and '.conf' not in file[0]:
                        print_msg(kwargs['runtime_verbose_msg'], 'Import file \''+ file[0] + '\'')
                else:
                    shutil.copy2(file, os.path.join(kwargs['log_path'], get_filename(file)))
                    if not kwargs.get('print_usage', False) and '.conf' not in file:
                        print_msg(kwargs['runtime_verbose_msg'], 'Import file \''+ file + '\'')
            except:
                print_msg(kwargs['runtime_verbose_msg'], "WARNING: Unable to copy file: " + file)

    # create an empty text file with filename = description
    # actual_log_path is only defined once for each set of experiments (i.e, once for all repetitions), thus this code will only run once
    if kwargs.get('description', None) and kwargs.get('actual_log_path', None):
        f = open(os.path.join(kwargs['actual_log_path'], '..', kwargs['description']), 'a')
        # f.write("Now the file has more content!")
        f.close()

    # modify logger.conf to set logfile location to log_path
    kwargs['log_conf'] = os.path.join(kwargs['log_path'], get_filename(generic_files['log_conf']))
    kwargs['learner_conf'] = os.path.join(kwargs['log_path'], get_filename(generic_files['learner_conf']))
    modify_logger_conf(kwargs['log_conf'], os.path.join(kwargs['log_path'], generated_files['log'][0]))
    modify_logger_conf(kwargs['learner_conf'], os.path.join(kwargs['log_path'], generated_files['log'][-1]))

    # get commands
    cmdArgs = get_cmd_for_client(**kwargs)
    cmdArgs.append(get_cmd_for_algo(**kwargs))
    if kwargs.get('multi_planning', None):
        if 'hybrid' in kwargs['multi_planning']:
            planner_ = kwargs['planner']
            if 'uct' in kwargs['multi_planning']:
                kwargs['planner'] = 'uct'
            else:
                kwargs['planner'] = 'prost'
            cmdArgs.append(get_cmd_for_algo(**kwargs))  # add hybrid PROST to cmd args
            kwargs['planner'] = planner_
    cmdline = ''
    for arg in cmdArgs:
        cmdline += arg + ' '
    if kwargs.get('print_usage', False):
        print(cmdline+'\n')
        return 1
    
    # write Python msg to console log
    f = open(os.path.join(kwargs['log_path'], logfile), 'w+')
    verbose_msgs = kwargs.get('verbose_msg', []) + kwargs.get('runtime_verbose_msg', [])
    if verbose_msgs:
        verbose_msgs.insert(0, '-------------------------------- WARNING --------------------------------')
        verbose_msgs.append('-------------------------------- WARNING --------------------------------\n')
    for msg in verbose_msgs:
        f.write(msg+'\n')
    f.close()
    if verbose_msgs:
        time.sleep(3)                                                                # allow time to read warning msg

    # piping
    # cmdline = cmdline + ' >> ' + os.path.join(kwargs['log_path'], logfile)         # use >> to append to file
    # cmdline = cmdline + ' | tee -a ' + os.path.join(kwargs['log_path'], logfile)   # this allows output to file and to console
    # print_msg(kwargs['verbose_msg'], "Piping outputs to " + logfile)
    
    # run executable
    try:
        time.sleep(kwargs.get('client_sleep', 0))                                    # allow server to load .rddl
        res = subprocess.call(cmdline, shell=True)
        if (res != 0):
            print("Unexpected error")
    #        if not DISABLE_LIBNOTIFY:
    #            Notify.init("MBRRL")
    #            notify_msg = Notify.Notification.new("mbrrl","Unexpected error! ","dialog-error")
    #            notify_msg.show ()
    #        raise RuntimeError
    except KeyboardInterrupt:
        print("\nUser terminated program!")
        return 0
    except:
        print("\nMain Program crashed due to unknown reason!")
        return 0

    # create folder results/experiment_problem_num
    if kwargs['policy'] is None:
        dest_folder = 'experiment_' + kwargs['domain'] + '_' + kwargs['planner']
    else:
        dest_folder = 'experiment_' + kwargs['domain'] + '_' + kwargs['planner'] + '_' + kwargs['policy']
    tmp_files_ = [os.path.join(kwargs['log_path'], f) for f in tmp_files]
    _, desc = get_summary_of_experiment(**kwargs)
    finish_experiment(os.path.join(kwargs['log_path'], '..', kwargs['domain']), kwargs['log_path'], dest_folder, \
                      kwargs['generated_files'], kwargs['generated_files_pattern'], tmp_files_, template_files_, desc)
    return 1


def finish_experiment(root_path, src_path, dest_folder, save_files, save_files_pattern, tmp_files, template_files_, desc = None):
    if not os.path.exists(root_path):
        os.makedirs(root_path, exist_ok=True)
    numbered_dest_folder = get_folder_with_numbering(root_path, dest_folder+'_')
    dest_path = os.path.join(root_path, numbered_dest_folder)      # results/domain/experiment_problem_num
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)

    remove_files(files = tmp_files, verbose = False)
    copy_files(save_files, src_path, dest_path, False)
    for file_pattern in save_files_pattern:
        copy_files(glob.glob(os.path.join(src_path, file_pattern)), '', dest_path, False)
    for file in template_files_:
        if '.cfg' in file:
            copy_files([file], src_path, dest_path)
            break
    if desc:
        f = open(os.path.join(root_path, summary_file), 'a+')
        f.write('Folder: ' + dest_path+'\n     '+desc+'\n')
        f.close()
    if working_path != mbrrl_path:
        dest_path2 = root_path.replace(working_path, mbrrl_path)
        if os.path.exists(dest_path2):
            new_numbered_dest_folder = get_folder_with_numbering(dest_path2, dest_folder+'_')
            # change numbering in working_path as mbrrl_path already has experiment folders
            os.rename(os.path.join(root_path, numbered_dest_folder), os.path.join(root_path, new_numbered_dest_folder))
            numbered_dest_folder = new_numbered_dest_folder
        move_folders(numbered_dest_folder, root_path, dest_path2)   # move folders to avoid storing too much files in /scratch
        copy_files(summary_file, root_path, dest_path2)
        os.makedirs(dest_path, exist_ok=True)                       # create empty folder back to retain numbering of folders else it will always be 0001 as we moved the folder
        # remove_all_files_in_folder(src_path, True)                # remove contents to avoid storing too much files in /scratch
        shutil.rmtree(src_path)                                     # remove folder to avoid storing too much files in /scratch
    print("Finished experiment.")


def get_folder_with_numbering(root_path, folder_name):
    # ps=os.popen('ls '+root_path+' | grep ' + current_result_dir + ' | cut -d "_" -f4 2>/dev/null')
    ps = os.popen('ls '+root_path+' | grep ' + folder_name)
    folders = ps.readlines()
    num = 0
    for folder in folders:
        try:
            num = max(num, int(folder[-4:]))
        except:
            continue
    num += 1
    num_str = "%04d" % (num)
    return folder_name + num_str


def get_summary_of_experiment(**kwargs):
    now = datetime.now()
    short_desc = str(now.strftime("%d/%m/%Y %H:%M:%S")) + ', Port: ' + str(kwargs['simulator_port']) + ', '
    desc = ''
    problem = ''
    if kwargs.get('problem', None):
        problem = list2string([p.strip().replace(kwargs['domain']+'_inst_mdp__', '') for p in kwargs['problem'].split(' ')], sort = False, linebreak = False, delimiter = ' ')
    if kwargs.get('domain', None):
        if problem:
            problem = 'Problem: ' + kwargs['domain'] + '_inst_' + problem
        else:
            problem = 'Domain: ' + kwargs['domain']
    if problem:
        desc += problem
        short_desc += problem
    if kwargs.get('initial_domain', None):
        phrase = ", Initial Domain: " + kwargs['initial_domain']
        desc += phrase
        short_desc += phrase
    if kwargs.get('planner', None):
        phrase = ", Planner: " + kwargs['planner']
        desc += phrase
        short_desc += phrase
    if kwargs.get('policy', None):
        desc += ", Policy: " + kwargs['policy']
    if kwargs.get('experience', None):
        desc += ", Experience: " + kwargs['experience']
    if kwargs.get('model_representation', None):
        desc += ", Model Representation: " + kwargs['model_representation']
    if kwargs.get('learner', None):
        desc += ", Learner: " + kwargs['learner']
    if kwargs.get('learn_from_failure', None):
        desc += ", LfF: " + xstr(kwargs['learn_from_failure'])
    # if kwargs.get('function_approximation', None):
    #     phrase = ", FA: " + kwargs['function_approximation']
    if kwargs.get('features_learner', None):
        phrase = ", FL: " + kwargs['features_learner']
        phrase_ = ''
        # if kwargs.get('lfa_common_learning', None):
        #     phrase += "-SL"
        # else:
        #     phrase += "-DSL"
        if kwargs.get('lfa_base_features', None):
            phrase_ += kwargs['lfa_base_features']
            put_underscore = True
        if kwargs.get('lfa_aggressive_pruning', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'P'
        if kwargs.get('lfa_first_order_features', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'L'
        if kwargs.get('lfa_asymmetric_update', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'A'
        if kwargs.get('lfa_use_non_fluents', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'S'
        if kwargs.get('lfa_use_neg_features', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'N'
        if kwargs.get('lfa_use_decoupled_weights', None):
            if put_underscore:
                put_underscore = False
                phrase_ += '_'
            phrase_ += 'D'
        if phrase_:
            phrase += ' (' + phrase_ + ')'
        phrase_ = ''
        phrase_ += kwargs.get('lfa_free_var_substitution', '')
        if kwargs.get('lfa_conflict_resolution_level', 3) != 3:
            phrase_ += '-CRL'+str(kwargs['lfa_conflict_resolution_level'])
        if kwargs.get('ifdd_discovery_threshold', None):
            if phrase_:
                phrase_ += ' '
            phrase_ += 'tau=' + str(kwargs['ifdd_discovery_threshold'])
        if kwargs.get('ifdd_max_features_addition', None):
            if phrase_:
                phrase_ += ' '
            phrase_ += 'kappa=' + str(kwargs['ifdd_max_features_addition'])
        if phrase_:
            phrase += ' (' + phrase_ + ')'
        desc += phrase
        short_desc += phrase
    if kwargs.get('multi_planning', None):
        desc += ", Plan Rollout: " + kwargs['multi_planning']
        short_desc += ", Plan Rollout: " + kwargs['multi_planning']
    if kwargs.get('intrinsic_reward_types', None):
        phrase = ", Intrinsic: " + list2string(kwargs['intrinsic_reward_types'])
        desc += phrase
        short_desc += phrase
    return short_desc, desc



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
                try:
                    return param + ' = ' + list2string(value, sort=False, linebreak=False, delimiter=' ') + '\n'
                except TypeError:
                    print('TypeError at Line 655')
                    print('param is:')
                    print(param)
                    print('value is:')
                    print(list2string(value, sort=False, linebreak=False, delimiter=' '))
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
            line = PHRASE+ "\"" + os.sep + logfilename + "\"\n"        # TODO
        destination.write(line)
    # close files and overwrite original .cfg file
    source.close()
    destination.close()
    shutil.move(filename+'~', filename)


def get_cmd_for_client(**kwargs):
    cmdArgs = [kwargs['bin_copy']]
    # cmdArgs.append(kwargs.get('log_path', None))
    # if cmdArgs[1] is None:
    #     raise Exception('log_path must be given.')
    # cmdArgs.append(kwargs.get('config_file', None))
    # if cmdArgs[2] is None:
    #     raise Exception('config_file must be given.')
    cmd_client_args = {}
    non_optional_client_args = {}
    config_args = {}
    num_non_optional_args = 0;
    for key, value in def_client_args.items():
        if value[0] is None:
            continue
        elif isinstance(value[0], int):
            # to be passed in as non-optional arguments in command line
            non_optional_client_args[value[0]] = kwargs.get(key, None)
            num_non_optional_args = max(num_non_optional_args, value[0])
        elif value[0] == 'config':
            # to be overwritten in .cfg file
            if kwargs.get(key, None) is not None and kwargs.get(key, None) != '':
                config_args[key] = kwargs[key]      # use user-defined value
            elif value[1] is not None and value[1] != '':
                config_args[key] = value[1]         # use default value
        elif isinstance(value[0], str):
            print('YES')
            # to be passed in as optional arguments in command line
            if kwargs.get(key, None) is not None and kwargs.get(key, None) != '':
                cmd_client_args[key] = kwargs[key]      # use user-defined value
            elif value[1] is not None and value[1] != '':
                cmd_client_args[key] = value[1]         # use default value
    if kwargs.get('problem', None):
        config_args['problem'] = kwargs['problem']

    for i in range(num_non_optional_args):
        cmdArgs.append(non_optional_client_args[i+1])
    
    # # overwrite value if given
    # for key in cmd_client_args:
    #     if key in kwargs:
    #         cmd_client_args[key] = kwargs[key]
    cmdline = ''
    for key in cmd_client_args:
        cmdline += get_flag_value(def_client_args, cmd_client_args, key)
    cmdArgs.append(cmdline)

    # modify config
    if True: # not kwargs.get('print_usage', False):
        modify_config(kwargs['config_file'], **config_args)

    return cmdArgs


def get_cmd_for_algo(**kwargs):
    planner = kwargs.get('planner', None)
    if planner is None:
        raise Exception('Planner argument must be provided.')
    else:
        # convert input to standard format that executable can read
        for key, values in alias.items():
            if planner in values:
                planner = key
    policy = kwargs.get('policy', 'null')
    if policy is None:
        policy = 'null'
    intrinsic_reward_types = kwargs.get('intrinsic_reward_types', 'null')
    if intrinsic_reward_types is None:
        intrinsic_reward_types = 'null'
    # get all applicable args given planner and policy
    cmd_algo_args = {}
    for key, value in def_algo_args.items():
        if len(value) == 2 or planner.lower() in value[2] or policy.lower() in value[2] or \
            at_least_one_common_element(intrinsic_reward_types, value[2]) or \
            policy == 'import' and key == 'plans_file':
            cmd_algo_args[key] = value[1]
    # overwrite value if given
    for key in cmd_algo_args:
        if key in kwargs:
            cmd_algo_args[key] = kwargs[key]
    # cmd_algo_args['seed'] += 10                     # change random seed without affecting which file gets imported
    cmdline = '"[' + planner + get_flag_value(def_algo_args, cmd_algo_args, 'seed')
    cmd_keys = list(cmd_algo_args.keys())
    cmd_keys.sort()
    for key in cmd_keys:
        if key != 'seed':
            cmdline += get_flag_value(def_algo_args, cmd_algo_args, key)
    return cmdline + ']"'


def get_flag_value(def_args, cmd_args, key):
    if cmd_args[key] is not None and def_args[key][0] != 'config' and not isinstance(def_args[key][0], int):
        return ' ' + str(def_args[key][0]) + ' ' + str(cmd_args[key])
    else:
        return ''

# -----------------------------
# -----------------------------
# -----------------------------
#       UTILITY
# -----------------------------
# -----------------------------
# -----------------------------

def print_msg(msgs, msg):
    msgs.append(msg)
    print(msg)


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


def at_least_one_common_element(list1, list2):
    if not isinstance(list1, list):
        list1 = [list1] 
    if not isinstance(list2, list):
        list2 = [list2]
    for x in list1: 
        for y in list2: 
            if x == y: 
                return True
    return False


def get_filename(file_path):
    if '/' in file_path:
        return file_path[file_path.rfind('/')+1:]
    elif '\\' in file_path:
        return file_path[file_path.rfind('\\')+1:]



# -----------------------------
# -----------------------------
# -----------------------------
#       FILES UTILITY
# -----------------------------
# -----------------------------
# -----------------------------


# clone folders in src_path to dest_path, including files in these folders
def clone_folders(folders, src_path, dest_path):
    if not isinstance(folders, list):
        folders = [folders]
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    for folder in folders:
        if not os.path.isdir(os.path.join(dest_path, folder)):
            os.makedirs(os.path.join(dest_path, folder), exist_ok=True)
        if os.path.isdir(os.path.join(src_path, folder)):
            files = [f for f in os.listdir(os.path.join(src_path, folder)) if os.path.isfile(os.path.join(src_path, folder, f) )]
            copy_files(files, os.path.join(src_path, folder), os.path.join(dest_path, folder))


def move_folders(folders, src_path, dest_path):
    if not isinstance(folders, list):
        folders = [folders]
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    for folder in folders:
        if os.path.isdir(os.path.join(src_path, folder)):
            shutil.move(os.path.join(src_path, folder), dest_path)


def copy_files(files, src_path, dest_path, verbose = True):
    if not isinstance(files, list):
        files = [files]
    for a_file in files:
        try:
            shutil.copy2(os.path.join(src_path, a_file), dest_path)
        except:
            try:
                shutil.copy2(a_file, dest_path)
            except:
                if verbose:
                    print("Warning: Couldn't copy " + os.path.join(src_path, a_file))


# create empty files
def create_files(files, path):
    if not isinstance(files, list):
        files = [files]
    for a_file in files:
        open(os.path.join(path, a_file), 'w').close()


def move_files(files, src_path, dest_path, verbose = True):
    if not isinstance(files, list):
        files = [files]
    for a_file in files:
        try:
            shutil.move(os.path.join(src_path, a_file), dest_path)
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
            os.remove(os.path.join(path, a_file))
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
        subfolder = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder):
            if os.path.isfile( os.path.join(folder, subfolder, filename) ):
                files.append(os.path.join(folder, subfolder, filename))
    return files


def append_list(list1, list2):
    if list1:
        if not isinstance(list1, list):
            list1 = [list1]
    else:
        list1 = []
    if list2:
        if not isinstance(list2, list):
            list2 = [list2]
    else:
        list2 = []
    return list1+list2



def main():
    print('Nothing to do')

if __name__ == "__main__":
    main()