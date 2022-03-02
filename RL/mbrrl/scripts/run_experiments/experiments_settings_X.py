#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:46:20 2019

@author: alvin
"""

import sys
import experiments_utils as exp_utils   # edit this file to specify filepaths and def arguments
import domains_utils                    # edit this file to specify folders and files for .rddl domains

# ----- GENERAL SETTINGS ----- #
use_release_bin = True
benchmark_dir = exp_utils.options['benchmark_dir'][1]
load_all_problems = False      # if true, load all problems to RDDLsim, else just load those in problems
num_reps = 10                  # no. of independent repetitions
num_rounds = 3000              # num of rounds per (random) instance
num_random_inst = 0            # num of randomized instances for each problem instance per repetition
random_reps = True             # True: randomized instance for each rep (not in use if num_random_inst > 0)
skip_experiments = []          # Vector of integers representing a list of repetition counts to skip, this is useful for continuing a set of experiments while correctly incrementing the parameters
save_optional_log = True       # True: save optional files (defined in experiments_utils.py as generated_files['optional'])
rpg_seed = None                # if None, then use repetition num as seed to random.sample RPG instances which will give a different set of random problems per rep
load_problems = False          # True: client will copy domain files to experiment folder (server will always copy), set to True for ROS experiments
description = None             # string describing experiment settings, this will create a textfile in the working_path which has filename = description 

# ----- PROBLEMS ----- #   FORMAT IS [domain1, domain2] or [(domain1, [list of instances]), (domain2, [list of instances])]
# If .rddl is not formatted correctly, set initial_domains = 'approx' and import_rddl_file = file path
# Example:
#        problems = exp_utils.options['problems']
#        problems = exp_utils.options['problems_ippc']
#        problems = [tiago_fetch', 'turtlebot_survey']
#        problems = [('tiago_fetch', ['p1','p2']), ('triangle_tireworld', [1,2,3])]
problems = [('robot_inspection', 3),      ('robot_inspection', 5),      ('recon2', 3),                ('recon2', 6),                # 0, 1, 2, 3
            ('grid_survey', 2),           ('grid_survey', 'sq5'),       ('taxi', 'sq3'),              ('taxi', 'sq5'),              # 4, 5, 6, 7
            ('academic_advising', 3),     ('academic_advising', 5),     ('triangle_tireworld', 3),    ('triangle_tireworld', 6),    # 8, 9, 10,11
            ('turtlebot_survey', 'de2'),  ('turtlebot_survey', 'de4'),  ('tiago_fetch', 'd1'),        ('tiago_fetch', 'd2'),        # 12,13,14,15
            ('tiago_hri', 1),             ('tiago_hri', 2),             ('tiago_hri', 3),                                           # 16,17,18
            ('blocksworld', 'unstack5'),  ('blocksworld',  'stack5'),   ('blocksworld', 'on5'),                                     # 19,20,21
            ('blocksworld', 'unstack10'), ('blocksworld',  'stack10'),  ('blocksworld', 'on10')]                                    # 22,23,24

# ----- MODEL -----
model_representations = ['list']
# experiences = exp_utils.options['experiences']
experiences = ['list']

# ----- PRIOR MODEL ----- #
# List of a set of prior models to use where the i-th element is for the i-th problem in problems
# Prior model is either a keyword (see domains_utils.py) or a .rddl file path
# If .rddl is not formatted correctly, set initial_domains = 'approx' and import_rddl_file = file path
# Example:
#        initial_domains = []                                 (use ground truth for all problems)
#        initial_domains = [['approx'], ['true', 'approx']]   (use approx for 1st problem, ground truth and approx for 2nd problem)
initial_domains = []

# ----- INTRINSIC REWARD ----- #
intrinsic_reward_types = []
# intrinsic_reward_types = exp_utils.options['intrinsic_reward_types']
# intrinsic_reward_types = [None, 'rmax', 'learner', ['rmax', 'learner']]

# ----- LEARNER ----- #
# lff               Learn from failure/deadend
# lff-bp'           Learn from failure/deadend with backpropagation
# lff-fo            Learn from failure/deadend with first-order generalization
# lff-bp-fo         Learn from failure/deadend with backpropagation & first-order generalization
# lfit / pasula     Model learners
learners = []
# learners = [[], ['lff'], ['lfit'], ['lff', 'lfit']]

# ----- PLAN ROLLOUT ----- #
# (multi_planning, beam_search_branch, num_hypothesis_domains, plan_rollout_horizon)
# plan_rollouts = [(None, 1, 0, 0), ('safe', 3, 3, 3), ('best', 3, 3, 3), ('common', 3, 3, 3), ('semihybrid', 1, 1, 1), ('hybrid', 1, 1, 1)]
plan_rollouts = []

# ----- FUNCTION APPROXIMXATION ----- #
# [FA_type or tuple] where tuple is holds any number of elements:
#       if element is string: FA_type OR base feature selector (only if using linear FA) OR substitution criteria (only if using first-order features)
#       if element is int:    prune step size
#       if element is bool:   value for lfa_common_learning
# FA_type: 'exact', 'neural_network', 'linear'
#
# base feature selector:
#       'all', 'param', 'cpf', 'import'
#    modifier:
#      int = hierarchy if using linear_cpf
#        p = 'lfa_aggressive_pruning'
#        l = 'lfa_first_order_features'
#        a = 'lfa_asymmetric_update'
#        s = 'lfa_use_non_fluents'
#        n = 'lfa_use_neg_features'
#        d = 'lfa_use_decoupled_weights'
# Example for base feature selector: 'cpf_2pls'
#
# Substitution Criteria (combination of any of the following delimited by -):
#       'or' (DEFAULT), 'sum'                                                         --> element-wise OR, SUM
#       '' (DEFAULT), 'qvalue', 'state', 'abs', 'specific'                            --> metric to maximize over
#       '' (DEFAULT), 'ground'                                                        --> use ground context
#       '' (DEFAULT), 'goal', 'goal-synergy', 'ordered-goal', 'given-ordered-goal'    --> use goal context, can add '-proximity' or/and '-all' to any options
#       '' (DEFAULT), 'location'                                                      --> use location context
#
# Use a tuple of numbers for the following parameters (must follow sequence but need not specify for all)
#       'ifdd_discovery_threshold'         
#       'ifdd_max_features_addition'       
#       'ifdd_max_feature_size'              
#       'ifdd_initial_feature_size'
#       'ifdd_batch_size'
#
# Use any tuple with 2 elements (key, value), for example, to set mqte_horizon to 3:
#       ('mqte_horizon', 3)

# key can also be tuple specifying domain and problem instance; make sure problem instance is consistent! str and int are not the same (i.e., '3' and 3)
# Example: keyed_function_approximations[('taxi', 'sq5')] or keyed_function_approximations[('taxi')]
keyed_function_approximations = {}
function_approximations = []

# ----- PLANNER ----- #
# planners = exp_utils.options['planners']
# planners = ['ql', 'qlearning', 'doubleq', 'dual-doubleq', 'dynaq', 'sarsa', 'sarsal'] #, 'rmax', 'vmax']
planners = ['doubleq']

# ----- POLICY ----- #
# policies = exp_utils.options['policies']
policies = ['epsilon']

# ----- SETTINGS ----- #
client_args = {
        # ---------- algo_args
        'seed': 1,
        'searchengine': '[IPPC2014]',
        # 'searchengine': '[THTS -act [UCB1] -out [UMC] -backup [PB] -init [Expand -h [IDS]]]',
        'alpha': 0.3,                                     # learning rate [used to be constant, now is linearly decaying]
        'discount': 0.9,                                  # discount factor [used to be 0.8, 0.9 is most commonly used]
        'lambda': 0.7,                                    # eligibility trace weightage [used to be 0.9, 0.7 is empirically the best in general]
        'tolerance': 0.001,                               # convergence test
        # 'rmax': 10,                                     # R-MAX & V-MAX's RMAX (deprecated, use max_intrinsic_reward instead)
        'visitation_threshold': 3,                        # put 1 if deterministic domain
        'depth': 15,                                      # Maximum search depth, if < 0, then this is equal to planning horizon
        'timeout': 10,                                    # Maximum runtime (seconds)
        'max_iteration': 0,                               # Maximum number of iterations and maximum number of expanded nodes
        'rollout_horizon': 10,                            # Maximum simulation rollout horizon
        'policy_rollout_horizon': 0,                      # Simulation rollout length using policy generated from Q-function instead of random policy
        'mixing_factor':  0,                              # Mixing factor for leaf node: (1-mixing)*rollout value + mixing*Q(s,a)
        'reuse_tree': 0,                                  # If 1, then reuse search tree from previous episode
        'prune_actions': 0,                               # If 1, then prune useless actions
        'early_termination': 0,                           # If 1, then terminate early if condition is satisfied
        'most_visited': 0,                                # If 1, then select most visited node rather than node with max value
        'deadend_reward': 0,                              # If 1, then overwrite deadend reward
        'batch': 1,                                       # if = 1, update target FA at the end of episode, else, randomly update a FA
        'dual': 0,                                        # = 1: use sum of FA as policy; = 0: consider ground FA as policy; if between 0 and 1: threshold for switching out of imported fixed policy (if applicable)
        'batch_size': 5,                                  # for experience replay, choose smaller value if deterministic domain
        'theta': 0.01,                                    # Threshold for change in Value to add to priority queue
        'temp': 5.0,                                      # Softmax temp (high temp -> more exploration)
        'epsilon': 1.0,                                   # Epsilon-greedy [Deepmind also uses 1.0 and decay from there]
        'fucb': 1.0,                                      # UCB coefficient
        'decay': 0.95,                                    # rate at which epsilon/temp decrease at the end of each round
        'policy': None,                                   # inherit from policies
        'import_policy': None,                            # location of policy file to import from
        'export_policy': None,                            # location of policy file to export to
        'import_qvalue': None,                            # location of q value file to import from (use absolute path to start importing from Round 1, set import_qvalue = export_qvalue to rollover Qval from previous sessions)
        'export_qvalue': 'qvalue_approximation.dat',      # location of q value file to export to
        'import_intrinsic_reward': None,                  # location of intrinsic reward file (this must be defined even if not in use to import from qvalue_approximation_intrinsic.dat)
        'export_intrinsic_reward': 'intrinsic_reward.dat',# location of intrinsic reward file
        'plans_file': None,                               # import plan

        # ---------- Misc
        'save_file': True,                                # Save files generated in each round
        'simulator_host': 'localhost',
        'simulator_port': 2323,
        'timed_constraints': None,                        # folder for file timed_constraints_*.txt (* is problem instance number) which specifices timed constraints
                                                          # Format "start_time: (action_or_state_fluent_name arg1 arg2)  [duration]", if start_time < 0, then this is a dynamic goal
                                                          # Format "Max Makespan = 1000" where 1000 is the max mission time in seconds
        'allow_latent_objects': None,                     # If true and problem has latent objects, discover latent objects online
        'allow_dynamic_constraints': None,                # If true and problem has dynamic goals, then dynamic goals are considered as dynamic time constrained goals

        # ---------- Verbose
        'verbose_state': 1,                               # 0: no print, 1: print state vector, [2]: print true state fluents, 3: print all state fluents
        'verbose_action': 1,                              # 0: no print, [1]: print Q-values of applicable actions, 2: print Q-values for model-based and model-free
        'verbose_step': 1,                                # 0: no print, [1]: print applicable actions / policy / Q-function step-update, 2: print details of applicable actions / policy, and 3: print Q-function step-update
        'verbose_search': 0,                              # 0: no print, [1]: print PROST search / MQTE result / UCT / rollout / self-play, 2: print MQTE/UCT search tree / details of self-play, 3: print more details of UCT search tree
        'verbose_analysis': 0,                            # 0: no print, [1]: print analysis (ordered goals, context, SIGMA, TD error), 2: print details, 3: print more details
        'verbose_hyothesis_model': 1,                     # 0: no print, 1: print details for multi-hypothesis model planning
        'verbose_debug': 0,                               # 0: no print, 1: print goal context for each action, 2: print active features, [3]: print active first-order features and their grounding, 4: print possible substitutions of first-order features
        
        # ---------- Training Data
        'all_transitions_file': None,                     # transition file to export to
        'import_transition_file': None,                   # transition file to import from
        'import_transition_folder': None,                 # location of root folder where folders containing transitions files are at
        'import_transitions_num': None,                   # Number of transitions to import (if None then imports all)
        'import_transition_reset': False,                 # If true, import transitions and learn RDDL model, then discard training data; otherwise, import and train Q-function
        'import_knowledge_folder': None,                  # location of root folder where folders containing import_qvalue file, tabu_file file, or/and import_intrinsic_reward files are at (* will be replaced by domain name)

        # ---------- Model
        'prune': False,                                   # set to True to allow RDDL parser to prune state and action fluents
        # 'initial_domain': None,                         # inherit from initial_domains
        'use_model_for_app_actions': True,                # set to True to use model to determine if action is applicable
        'use_model_for_prediction': True,                 # set to True to use model to predict s', r (required for self-play and pruning useless actions)
        'evaluate_model_prediction_error': False,         # evaluate model prediction error
        # 'mve_horizon': 0,                               # inherit from function_approximations
        # 'mqte_horizon': 0,                              # inherit from function_approximations
        'noop_actions_allowed': None,                     # set to True to allow NOOP actions to be selected (it will still be selected if its the only option)
        'sync_model': False,                              # if true, transition & reward matrices are constructed for every element, can be slow for large domains
        'record_transitions': False,                      # If true, record transitions
        'always_update_q': True,                          # if true, update Q-values even if action fail to execute
        # 'experience': 'list',                           # inherit from experiences
        'model_representation': None,                     # inherit from model_representations
        'import_multi_rddl': 0,                           # number of RDDL models to import (for multi-model planning)
        'import_rddl_file': None,                         # RDDL file to import
        'import_rddl_folder': None,                       # location of root folder where folders containing RDDL files are at (* will be replaced by domain name)
        'fix_rddl_domain': None,                          # If true, augment CPF from input RDDL domain file with remaining information from true RDDL domain file

        # ---------- Q-Value Function Approximation
        'online_q_update': True,                          # If true, update Q-values online. Otherwise, only update at the start if training data is provided, Q-values are imported, or performing self-play
        # 'function_approximation': 'exact',              # inherit from function_approximations
        # 'lfa_common_learning': None,                    # inherit from function_approximations
        # 'lfa_use_non_fluents': 2,                       # If == 1, include selective non-fluents in features, if == 2, include every non-fluent
        # 'lfa_use_decoupled_weights': None,              # inherit from function_approximations
        # 'lfa_free_var_substitution': None,              # inherit from function_approximations
        'lfa_conflict_resolution_level': None,            # Conflict resolution level between ground context and goal context if ground context takes precedence
        'lfa_max_num_free_var': 2,                        # max num. of free variables allowed in a first-order feature
        'lfa_batch_retrain': False,                       # if true, reset weights and relevance and replay at end of episode if new features are added during the episode
        # 'lfa_goal_sequence': None,                      # Sequence of goal fluents to be used for ordered goal context
        'lfa_mbfs_parameters': None,                      # Parameters for MBFS, strings of 1's and 0's to represent true/false, respectively ("include_precond", "include_precond_of_reward", "include_reward", "exclude_noop_arc", "include_coparents_of_state_fluent", "include_ancestors_of_state_fluent", "include_neighbours_of_ancestors_of_state_fluent", "include_coparents_of_immediate_child_fluent", "include_coparents_of_action"
        'lfa_import_weights': None,                       # If importing LFA, besides importing features, also import weights if this is true
        'eligibility_trace_type': 'replacing',            # Eligibility type (accumulating, replacing, or dutch)
        'allow_trivial_eligibility_update': True,         # If true, always perform n-step update, else do not perform if transition is trivial (i.e., s = s1 and reward = action cost)
        'reset_eligibility_trace_per_subgoal': False,     # If true, reset eligibility traces when a subgoal is achieved
        'revert_to_best_policy': False,                   # Revert to best previous policy if current policy deteriorates
        'replay_trajectory_to_goal': False,               # Replay observed trajectories reaching goals at end of episode for goals which are not achieved
        'max_replay_buffer': 500000,                      # Maximum number of most recent transitions for replay
        'training_ratio': 0.8,                            # Percentage of training data used for training
        'selection_ratio': 0.2,                           # Percentage of training data used for selection
        'testing_ratio': 0.0,                             # Percentage of training data used for testing
        'hidden_perceptrons_number': '12',                # Number of neurons in each hidden layer
        'max_epochs_number': 500,                         # Maximum no. of epoch for training
        'display_period': 100,                            # Number of epochs between the training showing progress

        # ---------- Features Learner
        'ifdd_discovery_threshold': 0.01,                 # iFDD parameter: discovery threshold
        'ifdd_max_features_addition': 10,                 # iFDD parameter: maximum number of features to add greedily each time (if 0, then no limit)
        'ifdd_max_feature_size': 3,                       # iFDD parameter: maximum number of fluents allowed per feature (set to 0 to disable learning features)
        'ifdd_initial_feature_size': 0,                   # iFDD parameter: maximum number of fluents allowed per feature which is added at the start
        'ifdd_batch_size': None,                          # iFDD parameter: batch learning size, set > 1 if using Batch-iFDD

        # ---------- Loop Detection
        'max_loop_size': 0,                               # Max. size of loop to detect
        'prune_useless_action': False,                    # If true, prune useless actions
        
        # ---------- Planning
        # 'multi_planning': 'safe',                       # inherit from plan_rollouts
        'self_play_horizon': 0,                           # no. of steps to do self-play to initialize Q-values
        'self_play_repetitions': 0,                       # no. of repetitions for self-play
        # 'plan_rollout_horizon': 0,                      # inherit from plan_rollouts
        'plan_rollout_max_attempt': 1,                    # no. of attempts to try plan rollout if it fails
        
        # ---------- Temporal Reasoning
        'max_action_duration': None,                      # Maximium duration expected (seconds) which is used to normalize action cost, set to 0 to exclude duration as cost

        # ---------- Learners
        # 'learner': None,                                # inherit from learners
        # 'learn_from_failure': None,                     # inherit from learners
        # 'use_first_order_failure': None,                # inherit from learners
        # 'backpropagate_failure': None,                  # inherit from learners
        'learner_timeout': None,                          # Timeout in seconds for model learner
        'tabu_file': 'tabu.dat',                          # Import/export TABU from/to this file
        'learner_output_file': None,                      # Logfile for rules learner output
        'learning_step_size': 30,                         # Learn a model after the accumulated number of transitions for an action since the last learning took place equals this number
        'max_round_for_learning': 20,                     # Perform model learning up till this number of rounds (set -1 or None to disable learning)
        # 'beam_search_branch': 1,                        # inherit from plan_rollouts
        # 'num_hypothesis_domains': 0,                    # inherit from plan_rollouts

        # ---------- Local Minimum Detection
        'use_local_min_detection': False,                 # Set to true to detect local minimum and wipe slate clean
        'local_min_avg_visit_threshold': 5,               # If average number of visits for each state exceeds this number, then policy is looping
        'local_min_no_goal_threshold': 10,                # If number of successive rounds where goal is not reached exceeds this threshold, then local minimum is likely
        'local_min_stationary_policy_threshold': 1,       # If number of successive rounds where policy is unchanged, then policy might be stationary
        'local_min_non_goal_penalty': 0,                  # Reward for not reaching goal at end of episode

        # ---------- Intrinsic Reward
        'intrinsic_reward_types': None,                   # inherit from intrinsic_reward_types
        'intrinsic_reward_coefficent': 1.0,               # Coefficient for intrinsic reward: r = r_extrinsic + coeff * r_intrinsic
        'intrinsic_reward_coefficent_decay': None,        # Decay factor for coefficient for intrinsic reward
        'intrinsic_reward_aggregation': None,             # Aggregation method for multiple types of intrinsic reward: average or max
        'reward_for_failed_execution': None,              # reward for failed execution
}





##################################################################################################################################





# ----- OVERWRITE SETTINGS ----- #
# Delimit sub-choices with _ (e.g., mmp_true_transfer, kr_best)
# First sub-choice matters most
setting_choice        = 'kr_best'
# setting_choice        = 'kr_best_learned'
# setting_choice        = 'prl_dyna_learned'
# setting_choice        = 'transfer-learning'
# setting_choice        = 'transfer-learning_dyna_learned'
# setting_choice        = 'knowledge-transfer'
# setting_choice        = 'intrinsic'
# setting_choice        = 'dyna_best_learned'
# setting_choice        = 'uct_true'
# setting_choice        = 'mmp_dbn_transfer_best_true'
# setting_choice        = 'mmp_dbn_transfer_best_true_dual'
# setting_choice        = 'mmp_dbn_transfer_best_learned'
# setting_choice        = 'mmp_dbn_transfer_best_learned_dual'
# setting_choice        = 'ros_transfer-learning_diff'
# setting_choice        = 'ros_transfer-learning_diff_mmp_learned'
# setting_choice        = 'ros_knowledge-transfer_split'
# setting_choice        = 'compute-vd'

urgent                = False                      # Recommended value = False
num_split_learning    = 0                          # learn over different instances of the same scale within num_rounds
use_latent_model      = True                       # use latent RDDL model instead of true RDDL model (for Tiago HRI only), Recommended value = True 
use_ifdd              = True                       # Recommended value = True
use_neg_features      = True                       # Recommended value = True
use_decoupled_weights = False                      # Recommended value = False
use_SL                = True                       # Recommended value = True
use_MBFS              = False                      # Recommended value = False
use_adaptive_ifdd     = True                       # Recommended value = True
use_preload           = False                      # Recommended value = False
use_MVE               = False                      # Recommended value = False
use_MQTE              = True                       # Recommended value = True
use_MQTE_for_all      = False                      # Recommended value = False
use_MQTE_always       = False                      # Recommended value = False (use MQTE regardless of plateaus)
use_lfd               = False                      # Recommended value = False
transfer_lfd          = False                      # Recommended value = False (only for setting_choice = 'kr')
use_intrinsic         = False                      # Recommended value = False
use_vanilla_dyna      = False                      # Recommended value = False
use_real_condition    = False                      # Recommended value = False (i.e., expanding MDP with timed goals, for Tiago HRI only)
use_precondition      = True                       # Recommended value = True
client_args['allow_latent_objects'] = False        # Recommended value = False (i.e., expanding MDP, for Tiago HRI only)
client_args['dynamic_constraint_duration'] = 0     # Recommended value = 0
client_args['lfa_conflict_resolution_level'] = 3   # Recommended value = 3
model_representations = ['list']                   # Recommended value = 'list'
boost_performance   = False                        # Recommended value = False


############   NUM OF ROUNDS   ############
# num_reps = 1
# num_rounds = 500
# random_reps= False
# policies = ['greedy']


############   PROBLEMS   ############
urgent_problems = [('tiago_fetch', 'd2'), ('recon2', 6), ('turtlebot_survey', 'de4'), ('tiago_hri', 2), ('triangle_tireworld', 6), ('academic_advising', 5)]

if use_MQTE_for_all:
    domains_for_MQTE = ['robot_inspection', 'recon2', 'grid_survey', 'taxi', 'academic_advising', 'turtlebot_survey', 'tiago_fetch', 'tiago_hri', 'triangle_tireworld']
else:
    domains_for_MQTE = ['robot_inspection', 'recon2', 'grid_survey', 'taxi']


############   INTRINSIC   ############
intrinsic_types = ('intrinsic_reward_types', ['td_error', 'dowham'])
client_args['intrinsic_reward_aggregation'] = 'average' # average, max, or sum
# decay coefficient    
# client_args['intrinsic_reward_coefficent'] = 1
# client_args['intrinsic_reward_coefficent_decay'] = client_args['decay']
# do not decay coefficient
client_args['intrinsic_reward_coefficent'] = 0.1
client_args['intrinsic_reward_coefficent_decay'] = 1.0


############   MODEL-BASED   ############
MBFS = 'cpf_3'                                          # CPF3 for Tiago HRI, CPF2 for others
lfa_mbfs_parameters = '101000000'                       # include precond and reward cpf (for Tiago Fetch) (final version used, best config)
MQTE = [('mqte_horizon', 3)]
MVE = [('mve_horizon', 3)]
REXP = [('experience', 'relational')]
self_play = [('self_play_horizon', 40), ('self_play_repetitions', 1000)]
vanilla_self_play = [('self_play_horizon', -5), ('self_play_repetitions', -1)]

client_args['depth'] = 15                               # Maximum search depth, if < 0, then this is equal to planning horizon (RMAX, VMAX, PROST, UCT)
client_args['timeout'] = 10                             # Maximum runtime (seconds)
client_args['max_iteration'] = 10000                    # Maximum number of iterations and maximum number of expanded nodes
client_args['reuse_tree'] = 0                           # Recommended value = 0; If 1, then reuse search tree from previous episode (memory intensive!)
client_args['prune_actions'] = 0                        # Recommended value = 0; If 1, then prune useless actions
client_args['early_termination'] = 0                    # Recommended value = 0; If 1, then terminate early if condition is satisfied
client_args['most_visited'] = 0                         # Recommended value = 0; If 1, then select most visited node rather than node with max value
client_args['deadend_reward'] = 0                       # Recommended value = 0; If 1, then overwrite deadend reward
client_args['rollout_horizon'] = 5                      # Maximum simulation depth (UCT) (must simulate till end unless using Q-function)
client_args['policy_rollout_horizon'] = 5               # Simulation rollout length using policy generated from Q-function instead of random policy
client_args['mixing_factor'] = 0.5                      # Mixing factor for leaf node: (1-mixing)*rollout value + mixing*Q(s,a)


############   MODEL-FREE   ############
ifdd = [('ifdd_discovery_threshold', 3), ('ifdd_max_features_addition', 0)]
adaptive_ifdd = [('ifdd_discovery_threshold', 0.1), ('ifdd_max_features_addition', -5)]         # if tau is < 0, then tau = abs(tau)/100*max_{action}(base features)
preload_features = [('ifdd_max_feature_size', 2), ('ifdd_initial_feature_size', 2)]
criteria = '-or-'

# index (starts from 0) of CX_BASIC that is the best for a domain
best_function_approximation = {
    'academic_advising': 12,
    'blocksworld': 4,
    'triangle_tireworld': 4,
    'tiago_fetch': 12,
    'tiago_hri': 19,
    'others': 17,
}


############   TRANSFER LEARNING   ############
if 'nalvin' in exp_utils.working_path:
    import_knowledge_folder = '/home/nalvin/rrl/Results/small-scale-policy/*/'
    import_knowledge_folder_lfd = '/home/nalvin/rrl/Results/small-scale-lfd/*/'
elif '/home/alvin' in exp_utils.working_path:
    import_knowledge_folder = '/home/alvin/rrl/Results/small-scale-policy/*/'
    import_knowledge_folder_lfd = '/home/alvin/rrl/Results/small-scale-lfd/*/'
else:
    import_knowledge_folder = '/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/small-scale-policy/*/'
    import_knowledge_folder_lfd = '/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/small-scale-lfd/*/'

if transfer_lfd:
    TRANSFER = [('import_qvalue', 'qvalue_approximation.dat'), ('epsilon', 0.2), ('import_knowledge_folder', [import_knowledge_folder]+[import_knowledge_folder_lfd])]
    client_args['import_knowledge_folder'] = exp_utils.append_list(client_args['import_knowledge_folder'], import_knowledge_folder_lfd)
    client_args['tabu_file'] = 'tabu.dat'
else:
    TRANSFER = [('import_qvalue', 'qvalue_approximation.dat'), ('epsilon', 0.2), ('import_knowledge_folder', import_knowledge_folder)]
DUAL0 = [('dual', 0), ('planner', 'dual-doubleq')] + TRANSFER
DUAL1 = [('dual', 1), ('planner', 'dual-doubleq')] + TRANSFER


############   LEARN FROM DEADEND   ############
if use_lfd or transfer_lfd:
    # learners = [['lff']]
    # learners = [['lff-bp']]
    # learners = [['lff-fo']]
    learners = [['lff-bp-fo']]


############   VERBOSE   ############
# client_args['verbose_state'] = 3              # 0: no print, 1: print state vector, [2]: print true state fluents, 3: print all state fluents
# client_args['verbose_action'] = 2             # 0: no print, [1]: print Q-values of applicable actions, 2: print Q-values for model-based and model-free
# client_args['verbose_step'] = 1               # 0: no print, [1]: print applicable actions / policy / Q-function step-update, 2: print details of applicable actions / policy, and 3: print Q-function step-update
# client_args['verbose_search'] = 2             # 0: no print, [1]: print PROST search / MQTE result / UCT / rollout / self-play, 2: print MQTE/UCT search tree / details of self-play, 3: print more details of UCT search tree
# client_args['verbose_analysis'] = 2           # 0: no print, [1]: print analysis (ordered goals, context, SIGMA, TD error), 2: print details, 3: print more details
# client_args['verbose_hyothesis_model'] = 1    # 0: no print, [1]: print details for multi-hypothesis model planning
# client_args['verbose_debug'] = 1              # 0: no print, [1]: print goal context for each action, 2: print active features, [3]: print active first-order features and their grounding, 4: print possible substitutions of first-order features
if not client_args['use_model_for_app_actions']:
    client_args['verbose_action'] = 0           # 0: no print, [1]: print Q-values of applicable actions



##################################################################################################################################



GND_APPROX = [('linear', )]

# compare context
CX_BASIC = [('linear', criteria),                                              #1  (AA, TT, TS, HRI)
            
            ('linear', criteria+'-location'),                                  #2  (RI, RC, GS, TX, TT, TS, HRI)
            
            ('linear', criteria+'-goal'),                                      #3  (AA, TS, HRI)
            ('linear', criteria+'-ordered-goal'),                              #4  (AA, TT, TS, HRI)
            
            ('linear', criteria+'-ground'),                                    #5  (AA, TT, TS, HRI)             --> TT BEST
            
            ('linear', criteria+'-location-goal'),                             #6  (RI, RC, GS, TX, TS, HRI)
            ('linear', criteria+'-location-ordered-goal'),                     #7  (RI, RC, GS, TX, TS, HRI)
            ('linear', criteria+'-location-given-ordered-goal'),               #8  (RI, RC, GS, TX, TS, HRI)
            
            ('linear', criteria+'-location-ground'),                           #9  (RI, RC, GS, TX, TS, HRI)
            
            ('linear', criteria+'-goal-ground'),                               #10 (AA, TS, HRI)
            ('linear', criteria+'-ordered-goal-ground'),                       #11 (AA, TT, TS, HRI)
            ('linear', criteria+'-given-ordered-goal-ground'),                 #12 (AA, TS, HRI)
            
            ('linear', criteria+'-ground-goal'),                               #13 (AA, TS, HRI)                 --> AA, TF BEST
            ('linear', criteria+'-ground-ordered-goal'),                       #14 (AA, TT, TS, HRI)
            ('linear', criteria+'-ground-given-ordered-goal'),                 #15 (AA, TT, TS, HRI)
            
            ('linear', criteria+'-location-goal-ground'),                      #16 (RI, RC, GS, TX, TS, HRI)
            ('linear', criteria+'-location-ordered-goal-ground'),              #17 (RI, RC, GS, TX, TS, HRI)
            
            ('linear', criteria+'-location-ground-goal'),                      #18 (RI, RC, GS, TX, TS, HRI)     --> RC, TS BEST
            ('linear', criteria+'-location-ground-ordered-goal'),              #19 (RI, RC, GS, TX, TS, HRI)

            ('linear', criteria+'-ground-goal-location'),                      #20 (HRI)                         --> HRI BEST
            ('linear', criteria+'-ground-ordered-goal-location'),              #21 (HRI)

            ('linear', criteria+'-location-ground-proximity-goal'),            #22 (RI, RC, GS, TX, TS, HRI)
            ('linear', criteria+'-location-ground-proximity-ordered-goal'),    #23 (RI, RC, GS, TX, TS, HRI)

            ('linear', criteria+'-null')]                                      #24 for ablation study


# compare context and max-operator
CX_OPERATOR = []
modifier = ''
if use_neg_features:
    if use_decoupled_weights:
        modifier = '_plsnd'
    else:
        modifier = '_plsn'
else:
    if use_decoupled_weights:
        modifier = '_plsd'
    else:
        modifier = '_pls'
for v1 in ['or', 'or-specific', 'or-qvalue', 'sum', 'sum-specific', 'sum-qvalue']:
    FA_tmp = []
    for v2 in ['ground']:
        if use_MBFS:
            FA_tmp.append(('linear', MBFS+modifier, v1+'-'+v2))
        else:
            FA_tmp.append(('linear', 'all'+modifier, v1+'-'+v2))
        CX_OPERATOR.append(FA_tmp)             # size = len(v1) * len(v2)
    # CX_OPERATOR.append(FA_tmp)               # size = len(v1)
CX_OPERATOR = [v for TMP in CX_OPERATOR for v in TMP]           # this will unwrap list of list into list, since we are not using list of list anymore


# define intrinsic
intrinsic_reward_types_to_use = [                                                                # GND LFA       FO LFA           
    [],                                                                                          # 0             23
    [('intrinsic_reward_types', ['rmax'])],                                                      # 1             24
    [('intrinsic_reward_types', ['visit_count'])],                                               # 2             25
    [('intrinsic_reward_types', ['visit_count'])]+REXP,                                          # 3             26
    [('intrinsic_reward_types', ['goal_trajectory'])],                                           # 4             27
    [('intrinsic_reward_types', ['td_error'])],                                                  # 5             28
    [('intrinsic_reward_types', ['delta_td_error'])],                                            # 6             29
    [('intrinsic_reward_types', ['dowham'])],                                                    # 7             30

    [('intrinsic_reward_types', ['visit_count', 'goal_trajectory'])]+REXP,                       # 8             31
    [('intrinsic_reward_types', ['visit_count', 'td_error'])]+REXP,                              # 9             32
    [('intrinsic_reward_types', ['visit_count', 'delta_td_error'])]+REXP,                        # 10            33
    [('intrinsic_reward_types', ['td_error', 'goal_trajectory'])],                               # 11            34
    [('intrinsic_reward_types', ['delta_td_error', 'goal_trajectory'])],                         # 12            35
    [('intrinsic_reward_types', ['dowham', 'td_error'])],                                        # 13            36
    [('intrinsic_reward_types', ['dowham', 'delta_td_error'])],                                  # 14            37
    [('intrinsic_reward_types', ['dowham', 'goal_trajectory'])],                                 # 15            38

    [('intrinsic_reward_types', ['first_order_explore'])]+DUAL0,                                 # 16            [DO NOT USE]  (KTI: transfer first-order to use as intrinsic)
    [('intrinsic_reward_types', ['first_order_target'])]+DUAL0,                                  # 17            [DO NOT USE]
    [('intrinsic_reward_types', ['first_order_explore'])]+DUAL1,                                 # [DO NOT USE]  41            (TLI: transfer & learns first-order to use as intrinsic)
    [('intrinsic_reward_types', ['td_error, first_order_explore'])]+DUAL0,                       # 19            [DO NOT USE]  (KTI: transfer first-order to use as intrinsic)
    [('intrinsic_reward_types', ['td_error, first_order_target'])]+DUAL0,                        # 20            [DO NOT USE]
    [('intrinsic_reward_types', ['td_error, first_order_explore'])]+DUAL1,                       # [DO NOT USE]  44            (TLI: transfer & learns first-order to use as intrinsic)
    
    [('intrinsic_reward_types', ['visit_count', 'td_error', 'dowham', 'goal_trajectory'])],      # 22            45
]



##################################################################################################################################



if urgent and urgent_problems:
    problems = urgent_problems

if num_split_learning > 1:
    if num_rounds % num_split_learning > 0:
        raise Exception('Number of rounds = ' + str(num_rounds) + ' which is not divisible by num_split_learning = ' + str(num_split_learning))
    client_args['import_intrinsic_reward'] = 'intrinsic_reward.dat'             # this will perform transfer learning for intrinsic reward
    client_args['import_qvalue'] = 'qvalue_approximation.dat'                   # this will perform transfer learning from session to session, even for ground LFA, but not from the first session because client_args['import_knowledge_folder'] is not defined
    if urgent:
        problems = domains_utils.lsof_domains.getProblemInstances(problems, num_instances = num_split_learning, num_repetitions = num_reps, starting_seed = client_args['seed'], concatenate = True)
        random_reps = False
        num_reps = 1
    else:
        problems = domains_utils.lsof_domains.getProblemInstances(problems, num_instances = num_split_learning, num_repetitions = 1, starting_seed = client_args['seed'], concatenate = True)
    num_rounds = int(num_rounds / num_split_learning)
    print('Continual learning from scratch, no transfer for first problem, set import_knowledge_folder to None')
    import_knowledge_folder = None                                              # this will disable transfer learning for first episode
    if transfer_lfd:
        raise Exception('Not yet implemented for transferring LFD')
elif urgent:
    problems = domains_utils.lsof_domains.getProblemInstances(problems, num_instances = num_reps, num_repetitions = 1, starting_seed = client_args['seed'], concatenate = False)
    random_reps = False
    num_reps = 1

if use_ifdd:
    GND_APPROX =  [tuple(['ifdd+', use_SL]+list(v)) for v in GND_APPROX]
    CX_BASIC =    [tuple(['ifdd+', use_SL]+list(v)) for v in CX_BASIC]
    CX_OPERATOR = [tuple(['ifdd+', use_SL]+list(v)) for v in CX_OPERATOR]
    if use_preload:
        GND_APPROX =  [tuple(list(v)+preload_features) for v in GND_APPROX]
        CX_BASIC =    [tuple(list(v)+preload_features) for v in CX_BASIC]
        CX_OPERATOR = [tuple(list(v)+preload_features) for v in CX_OPERATOR]
    # CX_OPERATOR = [tuple(['ifdd+', use_SL]+list(v)) for TMP in CX_OPERATOR for v in TMP]    # this will unwrap list of list into list
    if use_adaptive_ifdd:
        GND_APPROX = [tuple(list(v)+adaptive_ifdd) for v in GND_APPROX]
        CX_BASIC = [tuple(list(v)+adaptive_ifdd) for v in CX_BASIC]
        CX_OPERATOR = [tuple(list(v)+adaptive_ifdd) for v in CX_OPERATOR]
    else:
        GND_APPROX = [tuple(list(v)+ifdd) for v in GND_APPROX]
        CX_BASIC = [tuple(list(v)+ifdd) for v in CX_BASIC]
        CX_OPERATOR = [tuple(list(v)+ifdd) for v in CX_OPERATOR]

if use_MQTE_always:
    use_MQTE = True
    MQTE = tuple((MQTE[0], list(MQTE)[1]*-1))

if use_MVE:
    GND_APPROX =  [tuple(list(v)+MVE) for v in GND_APPROX]
    CX_BASIC =    [tuple(list(v)+MVE) for v in CX_BASIC]
    CX_OPERATOR = [tuple(list(v)+MVE) for v in CX_OPERATOR]

if use_MBFS:
    client_args['lfa_mbfs_parameters'] = lfa_mbfs_parameters
    if use_neg_features:
        GND_APPROX = [tuple(list(v)+[MBFS+'_n']) for v in GND_APPROX]
    else:
        GND_APPROX = [tuple(list(v)+[MBFS]) for v in GND_APPROX]
    KR = [tuple(list(v)+[MBFS+modifier]) for v in CX_BASIC]
else:
    if use_neg_features:
        GND_APPROX = [tuple(list(v)+['all_n']) for v in GND_APPROX]
    else:
        GND_APPROX = [tuple(list(v)+['all']) for v in GND_APPROX]
    KR = [tuple(list(v)+['all'+modifier]) for v in CX_BASIC]

if not use_precondition:
    num_rounds = 5000
    client_args['ifdd_max_feature_size'] = 5
    client_args['use_model_for_app_actions'] = False

if use_intrinsic:
    GND_APPROX = [tuple(list(v)+[intrinsic_types]) for v in GND_APPROX]
    # KR = [tuple(list(v)+[intrinsic_types]+REXP) for v in KR]
    KR = [tuple(list(v)+[intrinsic_types]) for v in KR]

if use_real_condition:
    client_args['allow_latent_objects'] = True          # (i.e., expanding MDP, for Tiago HRI only)
    client_args['dynamic_constraint_duration'] = 300

if boost_performance:
    model_representations = ['dbn']
    client_args['allow_trivial_eligibility_update'] = False
    client_args['reset_eligibility_trace_per_subgoal'] = True
    client_args['prune_useless_action'] = True
    client_args['max_loop_size'] = 4

description = 'description: ' + setting_choice



##################################################################################################################################



# ----- EXPERIMENTS ----- #
setting_choice = setting_choice.split('_')

if 'learned10' in setting_choice:
    import_rddl_folder = exp_utils.mbrrl_path + '/domains/learned_10/*'
elif 'learned50' in setting_choice:
    import_rddl_folder = exp_utils.mbrrl_path + '/domains/learned_50/*'
elif 'learned' in setting_choice:
    import_rddl_folder = exp_utils.mbrrl_path + '/domains/learned/*'


if 'kr' == setting_choice[0]:
    description += ' - test contextual grounding'
    if 'best' in setting_choice:
        for domain in best_function_approximation:
            if domain == 'others':
                function_approximations = GND_APPROX + [KR[best_function_approximation[domain]]]
            else:
                keyed_function_approximations[domain] = GND_APPROX + [KR[best_function_approximation[domain]]]
    else:
        function_approximations = GND_APPROX+KR
    if use_MQTE:
        for domain in domains_for_MQTE:
            function_approximations_copy = keyed_function_approximations.get(domain, function_approximations)
            keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in function_approximations_copy]
    if use_vanilla_dyna:
        function_approximations = [tuple(list(v)+vanilla_self_play) for v in function_approximations]
        for domain in keyed_function_approximations:
            keyed_function_approximations[domain] = [tuple(list(v)+vanilla_self_play) for v in keyed_function_approximations[domain]]
    if 'true' in setting_choice:
        model_representations = ['dbn']
        client_args['use_model_for_prediction'] = True
        initial_domains = []
    elif 'approx' in setting_choice:
        model_representations = ['dbn']
        client_args['use_model_for_prediction'] = True
        initial_domains = [['approx']]
        client_args['prune'] = False
    elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
        model_representations = ['dbn']
        client_args['use_model_for_prediction'] = True
        client_args['import_rddl_folder'] = import_rddl_folder
        client_args['import_rddl_file'] = 'learned_domain.rddl'
        client_args['import_multi_rddl'] = 1
        client_args['prune'] = False
    elif use_vanilla_dyna:
        raise Exception('Must specify initial model: true, approx, or learned')
elif 'no-free-var' == setting_choice[0]:
    for domain in best_function_approximation:
        if domain == 'others':
            function_approximations = [KR[best_function_approximation[domain]]]
        else:
            keyed_function_approximations[domain] = [KR[best_function_approximation[domain]]]
    client_args['lfa_max_num_free_var'] = 0
elif 'prl' == setting_choice[0]:
    description += ' - Mixed Approx.'
    planners = ['dual-doubleq']
    if 'dyna' in setting_choice:
        model_representations = ['dbn']
        client_args['use_model_for_prediction'] = True
        client_args['epsilon'] = 0.2
        GND_APPROX = [tuple(list(v)+self_play) for v in GND_APPROX]
        KR = [tuple(list(v)+self_play) for v in KR]
        if 'true' in setting_choice:
            initial_domains = []
        elif 'approx' in setting_choice:
            initial_domains = [['approx']]
            client_args['prune'] = False
        elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
            client_args['import_rddl_folder'] = import_rddl_folder
            client_args['import_rddl_file'] = 'learned_domain.rddl'
            client_args['import_multi_rddl'] = 1
            client_args['prune'] = False
        else:
            raise Exception('Must specify initial model: true, approx, or learned')
    # 0: Dual, no transfer (legend = D)
    # 1: Knowledge Transfer, Dual, Fixed Policy-Switch (legend = KTS)
    # 2: Knowledge Transfer, Dual, Fixed Policy-Sum (legend = KTD)
    # 3: Transfer Learning, Dual, Update Policy-Sum (legend = TLD)
    for domain in best_function_approximation:
        if domain == 'others':
            function_approximations = \
                [tuple(list(v) + [('dual', 1)]) for v in [KR[best_function_approximation[domain]]]] + \
                [tuple(list(v) + TRANSFER + [('dual', 0.25)]) for v in GND_APPROX] + \
                [tuple(list(v) + TRANSFER + [('dual', 1)]) for v in GND_APPROX] + \
                [tuple(list(v) + TRANSFER + [('dual', 1)]) for v in [KR[best_function_approximation[domain]]]]
        else:
            keyed_function_approximations[domain] = \
                [tuple(list(v) + [('dual', 1)]) for v in [KR[best_function_approximation[domain]]]] + \
                [tuple(list(v) + TRANSFER + [('dual', 0.25)]) for v in GND_APPROX] + \
                [tuple(list(v) + TRANSFER + [('dual', 1)]) for v in GND_APPROX] + \
                [tuple(list(v) + TRANSFER + [('dual', 1)]) for v in [KR[best_function_approximation[domain]]]]
elif 'knowledge-transfer' == setting_choice[0] or 'transfer-learning' == setting_choice[0]:
    if 'knowledge-transfer' in setting_choice:
        description += ' - Knowledge Transfer'
        policies = ['greedy']
        client_args['dual'] = 1
        client_args['online_q_update'] = False
    else:
        description += ' - Transfer Learning'
        client_args['epsilon'] = 0.2
        client_args['online_q_update'] = True
    if 'dyna' in setting_choice:
        model_representations = ['dbn']
        client_args['use_model_for_prediction'] = True
        client_args['epsilon'] = 0.2
        GND_APPROX = [tuple(list(v)+self_play) for v in GND_APPROX]
        KR = [tuple(list(v)+self_play) for v in KR]
        if 'true' in setting_choice:
            initial_domains = []
        elif 'approx' in setting_choice:
            initial_domains = [['approx']]
            client_args['prune'] = False
        elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
            client_args['import_rddl_folder'] = import_rddl_folder
            client_args['import_rddl_file'] = 'learned_domain.rddl'
            client_args['import_multi_rddl'] = 1
            client_args['prune'] = False
        else:
            raise Exception('Must specify initial model: true, approx, or learned')        
    # function_approximations = GND_APPROX+KR
    # if use_MQTE:
    #     KR_MQTE = [tuple(list(v)+MQTE) for v in KR]
    #     for domain in domains_for_MQTE:
    #         keyed_function_approximations[domain] = GND_APPROX+KR_MQTE
    for domain in best_function_approximation:
        if domain == 'others':
            function_approximations = [KR[best_function_approximation[domain]]]
        else:
            keyed_function_approximations[domain] = [KR[best_function_approximation[domain]]]
    if use_MQTE:
        for domain in domains_for_MQTE:
            function_approximations_copy = keyed_function_approximations.get(domain, function_approximations)
            keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in function_approximations_copy]
    if 'dbn' in setting_choice:
        model_representations = ['dbn']         # this is needed for MQTE because max. likelihood model is not transferrable
    client_args['import_knowledge_folder'] = exp_utils.append_list(client_args['import_knowledge_folder'], import_knowledge_folder)
    # client_args['lfa_import_weights'] = False
    client_args['import_qvalue'] = 'qvalue_approximation.dat'
elif 'intrinsic' == setting_choice[0]:
    if 'transfer' in setting_choice:
        client_args['import_knowledge_folder'] = exp_utils.append_list(client_args['import_knowledge_folder'], import_knowledge_folder)
        client_args['import_intrinsic_reward'] = 'intrinsic_reward.dat'
        client_args['import_qvalue'] = 'qvalue_approximation.dat'
    function_approximations_gnd = []
    for ins in intrinsic_reward_types_to_use:
        function_approximations_gnd += [tuple(list(v)+ins) for v in GND_APPROX]
    for domain in best_function_approximation:
        function_approximations_fo = []
        for ins in intrinsic_reward_types_to_use:
            function_approximations_fo += [tuple(list(v)+ins) for v in [KR[best_function_approximation[domain]]]]
        if domain == 'others':
            function_approximations = function_approximations_gnd + function_approximations_fo
        else:
            keyed_function_approximations[domain] = function_approximations_gnd + function_approximations_fo
    if use_MQTE:
        for domain in domains_for_MQTE:
            function_approximations_copy = keyed_function_approximations.get(domain, function_approximations)
            keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in function_approximations_copy]
elif 'dyna' == setting_choice[0]:
    if 'true' in setting_choice:
        initial_domains = []
    elif 'approx' in setting_choice:
        initial_domains = [['approx']]
        client_args['prune'] = False
    elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
        client_args['import_rddl_folder'] = import_rddl_folder
        client_args['import_rddl_file'] = 'learned_domain.rddl'
        client_args['import_multi_rddl'] = 1
        client_args['prune'] = False
    else:
        raise Exception('Must specify initial model: true, approx, or learned')
    if 'multi' in setting_choice:
        client_args['num_hypothesis_domains'] = 3
        client_args['import_multi_rddl'] = 3
    model_representations = ['dbn']
    GND_APPROX = [tuple(list(v)+self_play) for v in GND_APPROX]
    KR = [tuple(list(v)+self_play) for v in KR]
    if 'best' in setting_choice:
        for domain in best_function_approximation:
            if domain == 'others':
                function_approximations = GND_APPROX + [KR[best_function_approximation[domain]]]
            else:
                keyed_function_approximations[domain] = GND_APPROX + [KR[best_function_approximation[domain]]]
    else:
        function_approximations = GND_APPROX+KR
    if use_MQTE:
        for domain in domains_for_MQTE:
            function_approximations_copy = keyed_function_approximations.get(domain, function_approximations)
            keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in function_approximations_copy]
    client_args['epsilon'] = 0.2
    if use_intrinsic and intrinsic_types:
        if 'dyna' in intrinsic_types[1]:
            client_args['epsilon'] = 1
elif 'prost' == setting_choice[0] or 'uct' == setting_choice[0]:
    description += ' - model-based planning'
    model_representations = ['dbn']
    policies = ['greedy']
    if 'true' in setting_choice:
        initial_domains = []
        if 'prost' in setting_choice:
            client_args['prune'] = True
    elif 'approx' in setting_choice:
        initial_domains = [['approx']]
        client_args['prune'] = False
    elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
        client_args['import_rddl_folder'] = import_rddl_folder
        client_args['import_rddl_file'] = 'learned_domain.rddl'
        client_args['prune'] = False
    else:
        raise Exception('Must specify initial model: true, approx, or learned')
    if 'prost' in setting_choice:
        planners = ['prost']
    else:
        planners = ['uct']
    function_approximations = GND_APPROX
elif 'mmp' == setting_choice[0]:
    description += ' - hybrid planning'
    if 'true' in setting_choice:
        initial_domains = []
        if 'prost' in setting_choice:
            client_args['prune'] = True
    elif 'approx' in setting_choice:
        initial_domains = [['approx']]
        client_args['prune'] = False
    elif 'learned' in setting_choice or 'learned10' in setting_choice or 'learned50' in setting_choice:
        client_args['import_rddl_folder'] = import_rddl_folder
        client_args['import_rddl_file'] = 'learned_domain.rddl'
        client_args['import_multi_rddl'] = 1
        client_args['prune'] = False
    else:
        raise Exception('Must specify initial model: true, approx, or learned')
    if 'dbn' in setting_choice:
        model_representations = ['dbn']
    # plan_rollouts = [('best', 1, 1, 1), ('best', 1, 3, 3), ('semihybrid', 1, 1, 1), ('semihybrid', 1, 3, 3), ('hybrid', 1, 1, 1), ('hybrid', 1, 3, 3)]
    plan_rollouts = [('uct-semihybrid', 1, 1, 1), ('uct-hybrid', 1, 1, 1), ('uct-linear-hybrid', 1, 1, 1)]
    # insert plan_rollouts into function_approximations
    # order of function approximation: <LFA0+Rollout0, LFA1+Rollout0, LFA0+Rollout1, LFA1+Rollout1>
    if 'best' in setting_choice:
        for domain in best_function_approximation:
            if 'transfer' in setting_choice:
                function_approximations_copy_copy = [KR[best_function_approximation[domain]]]
            else:
                function_approximations_copy_copy = GND_APPROX + [KR[best_function_approximation[domain]]]
            function_approximations_copy = []
            for pr in plan_rollouts:
                rollout = [('multi_planning', pr[0]), ('beam_search_branch', pr[1]), ('num_hypothesis_domains', pr[2]), ('plan_rollout_horizon', pr[3])]
                if 'transfer' in setting_choice:
                    function_approximations_copy += [tuple(list(v)+rollout+TRANSFER) for v in function_approximations_copy_copy]
                else:
                    function_approximations_copy += [tuple(list(v)+rollout) for v in function_approximations_copy_copy]
            if domain == 'others': 
                function_approximations = function_approximations_copy
            else:
                keyed_function_approximations[domain] = function_approximations_copy
    else:
        function_approximations = GND_APPROX+KR
        function_approximations_copy = []
        for pr in plan_rollouts:
            rollout = [('multi_planning', pr[0]), ('beam_search_branch', pr[1]), ('num_hypothesis_domains', pr[2]), ('plan_rollout_horizon', pr[3])]
            if 'transfer' in setting_choice:
                function_approximations_copy += [tuple(list(v)+rollout+TRANSFER) for v in function_approximations]
            else:
                function_approximations_copy += [tuple(list(v)+rollout) for v in function_approximations]
            function_approximations = function_approximations_copy
    plan_rollouts = []
    # change policy
    if 'transfer' in setting_choice and 'epsilon' in policies:
        client_args['epsilon'] = 0.2
    else:
        policies = ['greedy']
    if 'dual' in setting_choice:
        planners = ['dual-doubleq']
        function_approximations = [tuple(list(v) + [('dual', 1)]) for v in function_approximations]
        for domain in keyed_function_approximations.keys():
            keyed_function_approximations[domain] = [tuple(list(v) + [('dual', 1)]) for v in keyed_function_approximations[domain]]
    # if use_MQTE:
    #     KR_MQTE = [tuple(list(v)+MQTE) for v in KR]
    #     for domain in domains_for_MQTE:
    #         if domain in keyed_function_approximations:
    #             keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in keyed_function_approximations[domain]]
    #         else:
    #             keyed_function_approximations[domain] = [tuple(list(v)+MQTE) for v in function_approximations]
# elif 'ippc' == setting_choice[0]:
#     num_reps = 1
#     num_rounds = 100
#     model_representations = ['dbn']
#     initial_domains = []
#     planners = ['prost']
#     problems = []
#     domains = ['recon']
#     for domain in domains:
#         for i in range(10):
#             problems += [(domain, i+1)]
else:
    raise Exception('No matching values for setting choice \'' + exp_utils.list2string(setting_choice) + '\'')

if not use_release_bin:
    print('Warning: Using debug-compiled binary')