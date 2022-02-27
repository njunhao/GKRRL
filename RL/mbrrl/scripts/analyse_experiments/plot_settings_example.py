#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:10:13 2019

@author: alvin
"""

import copy   # deep copy
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

# logfiles from all folders will be analysed (useful for analysing across different experiment runs)
# FORMAT: list of strings OR list of 2-element tuple where (string for folder, list of numbers for which subfolder with such number will be analysed)
# Example: ('recon2', [1, 2]) --> then recon2/experiment_recon2_doubleq_epsilon_0001, recon2/experiment_recon2_doubleq_epsilon_0002 will be analysed
settings['folders_to_analyse'] = []
# settings['folders_to_analyse'].append('')

################# SET LEGEND #################
settings['legend_labels'] = []
# settings['legend_labels'] = [
#     r'$\overline{All}, \xi = 0.01, \kappa = 50$',
#     r'$\overline{DBN} \sim 3, \xi = 0.01, \kappa = 50$',
#     r'$\overline{All}, \xi = 3$',
#     r'$DBN \sim 3, \xi = 0.01, \kappa = 50$']

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
settings['plot_options'].append(['rewards', 'terminal', 'overlay'])
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
settings['plot_options'].append(['original_rewards', 'terminal', 'cross'])
settings['plot_options'].append(['rewards', 'terminal', 'cross'])
settings['plot_options'].append(['num_features_per_round', 'cross'])
settings['plot_options'].append(['terminal_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['succ_exec', 'cumsum', 'cross'])
# settings['plot_options'].append(['goal_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['deadend_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['non_goal_state', 'cumsum', 'cross'])

################# CHOOSE GENERIC PLOT SETTINGS #################
# available options: 'save', 'show_title', 'show_fig', 'show_grid', 'show_legend', 'show_legend_outside', 'save_legend_in_fig'
settings['generic_plot_options'] = ['save', 'show_grid', 'show_title', 'save_legend_in_fig']
# settings['generic_plot_options'] = ['save', 'show_grid']

############ CHOOSE HOW TO GROUP THE EXPERIMENTS ############
# these separates the plots by the identifier
# example, if we put 'planner', then we get a figure for each planner which can contain plots of different configurations of each planner
# this is also pass into MultiAnalysis and used to control what appears in legend
# any keys that are listed will not have its value listed in legend
# keys to use as conditions to group analyses with values of these keys matching
#       settings['grouping_keys'] = [
#          'domain', 'instance', 'is_multi_tasks', 'learn_from_failure', 'learner', 'planner', 'policy', 
#          'discount_factor', 'model_representation', 'experience', 'function_approximation', 'features_learner', 
#          'initial_domain', 'beam_search_branch', 'multi_planning', 'num_hypothesis_domains', 'rollout_horizon']
#       'function_approximation_feature_selection',       ALL, CPF, IMPORT
#       'function_approximation_feature_selection_mod',   L2SPAN
#       'function_approximation_context',                 goal, location, ground
#       'function_approximation_max_criteria',            OR, SUM, state, qvalue, abs
settings['grouping_keys'] = []
settings['grouping_keys'].append(['domain', 'instance'])
# compare context
settings['grouping_keys'].append(['domain', 'instance', 'initial_domain', 'planner', 'function_approximation_max_criteria', 'function_approximation_feature_selection'])
# compare MAX criteria
# settings['grouping_keys'].append(['domain', 'instance', 'initial_domain', 'planner', 'function_approximation_context', 'function_approximation_feature_selection'])
# compare MBFS vs MFFS
# settings['grouping_keys'].append(['domain', 'instance', 'initial_domain', 'planner', 'function_approximation_context', 'function_approximation_max_criteria'])
# compare within same feature selection
# settings['grouping_keys'].append(['domain', 'instance', 'initial_domain', 'planner', 'function_approximation_feature_selection'])

################# CHOOSE WHAT EXPERIMENTS TO PLOT #################
# any analysis that match these properties will be plotted
settings['filter_conditions'] = []
fc = aysT.filter_condition.copy()
# fc['function_approximation_feature_selection_mod'] = ['PLASN']
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
    'x_num_div': 6,
    'y_lim': None,                  # (y_min, y_max) or (y_min, y_max, y_div)
    'y_log_scale': False,
    'moving_avg_window': 10,        # only applied when plotting rewards or execution time
    'sci': True,                    # if true, use scientific ticks for y axis
    'show_title': False,
    'show_fig': False,
    'show_grid': False,
    'show_legend': False,
    'show_legend_outside': False,
    'save_legend_in_fig': False,
    'legend_ncol': 1,
    # list of legend labels (string) which set the of plotting
    # get legend labels from print_aggregated_analyses()
    # if no grouped_analysis has a legend in reorder_by_legend, a dummy plot will be used
    # if a grouped_analysis has a legend not in reorder_by_legend, then either plot at the end (reorder_by_legend = True) or discard (reorder_by_legend = False)
    # Example:
    #    'reorder_by_legend': [
    #        'FA=L2SPN (CX-Goal)', 
    #        'FA=L2SPN (CX-Goal-S)',
    #        'FA=L2SPN (CX-O-Goal)'
    #    ]
    'reorder_by_legend': None,
    'add_analysis_with_no_matching_legend': False,      # used with reorder_by_legend, if True, plot grouped_analysis with legend that is not in reorder_by_legend
    'overwrite_legends': settings['legend_labels'],
    # superceded by reorder_by_legend, use reorder_plots to match legend style with a grouped analysis
    # to know legend style for each #, run asyT.generate_all_legend_styles() in main function
    # set to value of -1 to skip a legend style
    'reorder_plots': False,
    # save figure settings
    'figsize': (8, 4),
    # 'figsize': (3, 2),
    'fontsize': 10,
    'dpi': 100,
    'format': 'png',
    # line settings
    'color': 'k',
    # 'linestyles': ['-', '-.', '--', ':'],
    'linestyles': ['-.', '--', ':'],
    'linewidth': 2,
    'marker': None,
    'alpha': 1,
    # analysis settings
    'mode': [],
    'remove_outlier': [0, 0]    # [num of argmin, num of argmax] to remove, otherwise use a num which is equivalent to [num, num]
}
###################################################