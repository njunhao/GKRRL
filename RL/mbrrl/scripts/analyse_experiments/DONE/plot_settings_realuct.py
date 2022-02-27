#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:10:13 2019

@author: alvin
"""

# missing runs for UCT transfer, TS and RC UCT-true is poor
# UCT transfer: only AA and TT is good
# use UCT most visited nodes instead?


import copy   # deep copy
import os
import analysis_type as aysT

settings = {}

############## CHOOSE PROPERTIES OF EXPERIMENTS TO ANALYSE ##############
settings['domains'] = []                        # set to empty to plot all
settings['planners'] = []
settings['policies'] = []

############## CHOOSE LOGFOLDERS TO ANALYSE ##############
settings['logfile'] = 'mbrrl.log'
# settings['logfile'] = 'mbrrl_console.log'     # full logfile, takes longer to parse
settings['quick_plotting'] = 0                  # if > 0, only plot folders with numbering that is a multiple of quick_plotting

if 'nalvin' in os.getcwd():
    root_folder = '/home/nalvin/rrl/Results/'
elif '/home/alvin' in os.getcwd():
    root_folder = '/home/alvin/rrl/Results/'
else:
    root_folder = '/media/alvin/HDD/Academics/PhD/Coding/Experiments/mbrrl/'

# logfiles from all folders will be analysed (useful for analysing across different experiment runs)
settings['folders_to_analyse'] = []
settings['folders_to_analyse'].append(root_folder+'v4-uct/TDORMDP-500ep/HRI-3')

################# SET LEGEND #################
# must be added to settings['plot_options']: settings['plot_options'].append(['time_taken_per_round', 'cumsum', 'cross', settings['legend_labels']])
settings['legend_labels'] = []
settings['legend_labels'] = [
    # r'THTS (oracle)',                         # baseline
    # r'RRL',                                   # baseline
    # r'RRL + UCT (oracle)',
    # r'RRL + UCT (learned)',
    r'THTS (oracle)',                           # baseline
    r'LQ-RRL',                                  # baseline
    r'GK-RRL+ (oracle)',
    r'GK-RRL+ (learned)',
]
y_lim = None
# y_lim = (-300, -100, 50)

################# CHOOSE METRIC TO PLOT #################
# Types of Metrics:
#     'rewards'                             immediate reward per step
#     'original_rewards'                    immediate reward per step without reward modification
#     'rewards_per_round'                   immediate reward per round
#     'original_rewards_per_round'          immediate reward per round without reward modification
#     'rewards_computation_time_per_round'  immediate reward per round / computation tie per round
#     'norm_rewards'                        normalized immediate reward (deprecated)
#     'succ_exec'                           successful execution = 1
#     'terminal_state'                      goal state = 1, deadend state = -1, otherwise = 0
#     'goal_state'                          goal state = 1, otherwise = 0
#     'deadend_state'                       deadend state = 1, otherwise = 0
#     'non_goal_state'                      goal state = 0, otherwise = 0
#     'execution_timestamp'                 execution time at end of episode (seconds)
#     'time_taken'                          time taken per session (seconds)
#     'computation_time_per_round'          computatonal time per round (seconds)
#     'num_features_per_round'              total number of features for all actions at the end of a round

# settings['plot_options'] is a list to determine what type of plots to generate
# to add new type, need to modify MultiAnalysis
settings['plot_options'] = []

#       SINGLE: each figure is a single plot of an experiment
# settings['plot_options'].append(['rewards', 'terminal'])

#       OVERLAY: each figure has overlaying plots of each experiment
# settings['plot_options'].append(['rewards', 'terminal', 'overlay'])
# settings['plot_options'].append(['num_features_per_round', 'terminal', 'overlay'])
# settings['plot_options'].append(['terminal_state', 'cumsum', 'overlay'])
# settings['plot_options'].append(['non_goal_state', 'cumsum', 'overlay'])

#       AGGREGATE: each figure is a plot of the aggregate of experiments with the same setting
# settings['plot_options'].append(['rewards', 'terminal', 'agg'])

#       VALUE: print last value of metric for each experiment
# settings['plot_options'].append(['terminal_state', 'cumsum', 'value'])
# settings['plot_options'].append(['execution_timestamp', 'value'])
# settings['plot_options'].append(['rewards', 'terminal', 'value'])

#       CROSS: each figure compares experiments with the same values for settings['grouping_keys']
settings['is_rpg'] = False            # settings['is_rpg'] = True to disable grouping by instances when plotting 'cross'
settings['plot_options'].append(['computation_time_per_round', 'cumsum', 'cross'])
settings['plot_options'].append(['execution_timestamp', 'cross'])
# settings['plot_options'].append(['original_rewards', 'terminal', 'cross'])
settings['plot_options'].append(['rewards', 'terminal', 'cross'])
settings['plot_options'].append(['num_features_per_round', 'cross'])
# settings['plot_options'].append(['terminal_state', 'cumsum', 'cross'])

# settings['plot_options'].append(['succ_exec', 'cumsum', 'cross'])
settings['plot_options'].append(['goal_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['deadend_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['non_goal_state', 'cumsum', 'cross'])

################# CHOOSE GENERIC PLOT SETTINGS #################
# available options: 'save', 'show_title', 'show_fig', 'show_grid', 'show_legend', 'show_legend_outside', 'save_legend_in_fig'
settings['generic_plot_options'] = ['save', 'show_grid', 'save_legend_in_fig']

############ CHOOSE HOW TO GROUP THE EXPERIMENTS ############
# these separates the plots by the identifier
# example, if we put 'planner', then we get a figure for each planner which can
# contain plots of different configurations of each planner
# this is also pass into MultiAnalysis and used to control what appears in legend
# any keys that are listed will not have its value listed in legend
# keys to use as conditions to group analyses with values of these keys matching
# settings['grouping_keys'] = [
#    'domain', 'instance', 'is_multi_tasks', 'learn_from_failure', 'learner', 'planner', 'policy', 
#    'discount_factor', 'model_representation', 'experience', 'function_approximation', 'features_learner', 
#    'initial_domain', 'beam_search_branch', 'multi_planning', 'num_hypothesis_domains', 'rollout_horizon']
settings['grouping_keys'] = []
settings['grouping_keys'].append(['domain', 'instance'])                                               # compare FA

################# CHOOSE WHAT EXPERIMENTS TO PLOT #################
# any analysis that match these properties will be plotted
settings['filter_conditions'] = []
fc = aysT.filter_condition.copy()
fc['function_approximation_feature_selection_mod'] = ['PLASN']
# settings['filter_conditions'].append(fc)
if not settings['filter_conditions']:
    settings['filter_conditions'] = [{}]

################# SET FIGURE PARAMETERS #################
settings['plot_settings'] = copy.deepcopy(aysT.def_plot_settings)
settings['plot_settings'] = {
    # figure layout
    'fig': None,
    'ax': None,
    'title': 'undef',
    'label': 'undef',
    'x_num_div': 4,
    'y_lim': y_lim,
    'y_log_scale': False,
    'moving_avg_window': 10,
    'sci': True,            # if true, use scientific ticks for y axis
    'show_title': False,
    'show_fig': False,
    'show_grid': False,
    'show_legend': False,
    'show_legend_outside': False,
    'save_legend_in_fig': False,
    'legend_ncol': 4,
    # list of legend labels (string) which set the of plotting
    # get legend labels from print_aggregated_analyses()
    # if no grouped_analysis has a legend in reorder_by_legend, a dummy plot will be used
    # if a grouped_analysis has a legend not in reorder_by_legend, then either plot at the end (reorder_by_legend = True) or discard (reorder_by_legend = False)
    'reorder_by_legend': [
        'MDL=Dbn, Ground-Truth, PROST~10, HM=1',
        'MDL=List, Latent, Double_Q-Learning2, FA=LFA-ALL_L2SPN (CX-Gnd-Goal-Loc, OR), FL=iFDD+ (SL, zeta=0.1, I=0, M=3, tau=2), Replacing, Epsilon-Greedy, Alpha=0.3, Epsilon=0.2, Import-Qfunction=True, Lambda=0.7, Horizon=60, Discount=0.9, HM=1',
        # 'MDL=Dbn, Ground-Truth, UCT~1.41421~10~60~10~100000, Epsilon=1.0, Horizon=60, MPS=none',
        'MDL=Dbn, Ground-Truth, UCT~1.41421~10~5~10~100000~MF0.5~PRH5+Double_Q-Learning2, FA=LFA-ALL_L2SPN (CX-Gnd-Goal-Loc, OR), FL=iFDD+ (SL, zeta=0.1, I=0, M=3, tau=2), Replacing, Alpha=0.3, Epsilon=0.2, Import-Qfunction=True, Lambda=0.7, Horizon=60, MPS=uct-hybrid',
        'MDL=Dbn, Learned, UCT~1.41421~10~5~10~100000~MF0.5~PRH5+Double_Q-Learning2, FA=LFA-ALL_L2SPN (CX-Gnd-Goal-Loc, OR), FL=iFDD+ (SL, zeta=0.1, I=0, M=3, tau=2), Replacing, Alpha=0.3, Epsilon=0.2, Import-Qfunction=True, Lambda=0.7, Horizon=60, MPS=uct-hybrid',
    ],
    'add_analysis_with_no_matching_legend': False,      # used with reorder_by_legend, if True, plot grouped_analysis with legend that is not in reorder_by_legend
    'overwrite_legends': settings['legend_labels'],
    # superceded by reorder_by_legend, use reorder_plots to match legend style with a grouped analysis
    # to know legend style for each #, run asyT.generate_all_legend_styles() in main function
    # set to value of -1 to skip a legend style
    'reorder_plots': None,
    # save figure settings
    # 'figsize': (8, 4),
    'figsize': (3, 2),
    'fontsize': 10,
    'dpi': 100,
    'format': 'png',
    # line settings
    'color': 'k',
    # 'linestyles': ['-', '-.', '--', ':'],
    'linestyles': ['-', '--'],
    'linewidth': 2,
    'marker': None,
    'alpha': 1,
    # analysis settings
    'mode': [],
    'remove_outlier': [0, 0]    # [num of argmin, num of argmax] to remove, otherwise use a num which is equivalent to [num, num]
}
###################################################