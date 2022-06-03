#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin
"""

import matplotlib
matplotlib.use('Agg')               # to allow matplotlib to run in server
import matplotlib.pyplot as plt
# plt.tight_layout()
# plt.autoscale()
#import matplotlib.transforms
from cycler import cycler           # to cycle over different color and line styles for multi-plots
import numpy as np
import itertools
import abstraction_types as absT
import copy   # deep copy
import os
import gc


ACTION_COST = -1


# keys to use as conditions to group analyses with values of these keys matching
# grouped analyses are considered as homogenous and will be aggregated
grouping_keys = ['logfolderID',
                 'instance',
                 'domain',
                 'num_sessions',
                 'num_episodes',
                 'num_steps',
                 'initial_domain',
                 'latent_objects',
                 'dynamic_constraints',
                 'learner',
                 'learn_from_failure',
                 'model_representation',
                 'experience',
                 'function_approximation',
                 'function_approximation_feature_selection',      # ALL, CPF, IMPORT
                 'function_approximation_feature_selection_mod',  # L2SPAN
                 'function_approximation_context',                # goal, location, ground
                 'function_approximation_max_criteria',           # OR, SUM, state, qvalue, abs
                 'features_learner',
                 'features_learner_sync_learning',
                 'features_learner_zeta',
                 'features_learner_initial_feature_size',
                 'features_learner_max_feature_size',
                 'features_learner_tau',
                 'eligibility_trace_type',
                 'loop_detection',
                 'replay_trajectory_to_goal',
                 'revert_to_best_policy',
                 'beam_search_branch',
                 'multi_planning',
                 'num_hypothesis_domains',
                 'rollout_horizon',
                 'max_round_for_ml',
                 'local_min_detection',
                 'intrinsic_reward',
                 'intrinsic_reward_rmax',
                 'intrinsic_reward_beta',
                 'intrinsic_reward_beta_decay',
                 # 'intrinsic_reward_experience',
                 'intrinsic_reward_aggregation',
                 'self_play',
                 'mve_horizon',
                 'mqte_horizon',
                 'parser',
                 'planner', 
                 'policy',

                 'alpha',
                 'batch',
                 'decay',
                 'epsilon',
                 'import_intrinsic_reward',
                 'import_qvalue',
                 'lambda',
                 'horizon',

                 'discount_factor',
                 'is_multi_tasks']

# for plotting against ACE
# grouping_keys = ['logfolderID',
#                  'domain',
#                  'num_sessions',
#                  'num_episodes',
#                  'planner']

# keys to overwrite def_plot_settings
plot_keys = ['agg', 'cross', 'overlay', 'value', 'concatenate', 'concatenate-agg', 'is_rpg', 'save', 'show_title', 'show_fig', 'show_grid', 'show_legend', 'show_legend_outside', 'save_legend_in_fig']

# values of these keys of analysis shall appear in filenames, titles & legends of plots
# order the keys matters and is the order of the values concatenated
title_keys = ['logfolderID',
              'instance',
              'domain',
              'initial_domain',
              'latent_objects',
              'dynamic_constraints',
              'learner',
              'learn_from_failure',
              'model_representation',
              'experience',
              'function_approximation',
              'function_approximation_feature_selection',
              'function_approximation_feature_selection_mod',
              'function_approximation_context',
              'function_approximation_max_criteria',
              'features_learner',
              'features_learner_sync_learning',
              'features_learner_zeta',
              'features_learner_initial_feature_size',
              'features_learner_max_feature_size',
              'features_learner_tau',
              'eligibility_trace_type',
              'loop_detection',
              'replay_trajectory_to_goal',
              'revert_to_best_policy',
              'beam_search_branch',
              'multi_planning',
              'num_hypothesis_domains',
              'rollout_horizon',
              'max_round_for_ml',
              'local_min_detection',
              'intrinsic_reward',
              'intrinsic_reward_rmax',
              'intrinsic_reward_beta',
              'intrinsic_reward_beta_decay',
              # 'intrinsic_reward_experience',
              'intrinsic_reward_aggregation',
              'self_play',
              'mve_horizon',
              'mqte_horizon',
              'parser',
              'planner',
              'policy',

              'alpha',
              'batch',
              'decay',
              'epsilon',
              'import_intrinsic_reward',
              'import_qvalue',
              'lambda',
              'horizon',

              'discount_factor']

# this is used for deciding figure filenames because filenames are too long if we use title_keys
shorten_title_keys = [
              'instance',
              'domain',
              'initial_domain',
              'learner',
              'learn_from_failure',
              'model_representation',
              'experience',
              'planner',
              'replay_trajectory_to_goal',
              'revert_to_best_policy']

# list down elements of title_keys to be excluded from legend
exclude_legend_keys = [] #['discount_factor', 'policy', 'function_approximation', 'features_learner']

# to be set in batch_plot.py, any analysis that match these properties will be plotted
filter_condition = {}
filter_condition['domain'] = None
filter_condition['instance'] = None
filter_condition['planner'] = None
filter_condition['policy'] = None
filter_condition['learner'] = None
filter_condition['learn_from_failure'] = None
filter_condition['model_representation'] = None
filter_condition['experience'] = None
filter_condition['function_approximation'] = None
filter_condition['function_approximation_feature_selection'] = None
filter_condition['function_approximation_feature_selection_mod'] = None
filter_condition['function_approximation_context'] = None
filter_condition['function_approximation_max_criteria'] = None
filter_condition['features_learner'] = None
filter_condition['features_learner_sync_learning'] = None
filter_condition['features_learner_zeta'] = None
filter_condition['features_learner_initial_feature_size'] = None
filter_condition['features_learner_max_feature_size'] = None
filter_condition['features_learner_tau'] = None
filter_condition['initial_domain'] = None
filter_condition['latent_objects'] = None
filter_condition['dynamic_constraints'] = None
filter_condition['beam_search_branch'] = None
filter_condition['multi_planning'] = None
filter_condition['num_hypothesis_domains'] = None
filter_condition['rollout_horizon'] = None
filter_condition['intrinsic_reward'] = None
filter_condition['intrinsic_reward_rmax'] = None
filter_condition['intrinsic_reward_beta'] = None
filter_condition['intrinsic_reward_beta_decay'] = None
# filter_condition['intrinsic_reward_experience'] = None
filter_condition['intrinsic_reward_aggregation'] = None

# display settings
def_plot_settings = {
    'fig': None,
    'ax': None,
    'title': 'undef',
    'label': 'undef',
    'x_num_div': 4,
    'y_lim': None,
    'y_log_scale': False,
    'moving_avg_window': 0,                             # only applied when plotting rewards
    'sci': True,                                        # if true, use scientific ticks for y axis
    'show_title': False,
    'show_fig': False,
    'show_grid': False,
    'show_legend': False,
    'show_legend_outside': False,
    'save_legend_in_fig': False,                        # save legend in a separate figure
    'legend_ncol': 1,
    # list of legend labels (string) which set the of plotting
    # get legend labels from print_aggregated_analyses()
    # if no grouped_analysis has a legend in reorder_by_legend, a dummy plot will be used
    # if a grouped_analysis has a legend not in reorder_by_legend, then either plot at the end (reorder_by_legend = True) or discard (reorder_by_legend = False)
    # Example:
    #    'reorder_by_legend': {
    #        'academic_advising_mdp': [
    #            'sensitivity-tau, FA=N, FL=iFDD+ (tau=1)',
    #            'sensitivity-tau, FA=L2SPN (CX-Gnd-Goal, OR), FL=iFDD+ (tau=1)',
    #            'adaptive-nil_AA-5, FA=N, FL=iFDD+ (tau=4)',
    #            'dummy', #'adaptive-nil_AA-5, FA=L2SPN (CX-Gnd-Goal, OR), FL=iFDD+ (tau=1)',     # this is tau=1 which is the exactly the same as another plot
    #            'sensitivity-tau, FA=N, FL=iFDD+ (tau=8)',
    #            'dummy',                                         # this will be tau=1 which is the exactly the same as another plot
    #            'sensitivity-tau, FA=N, FL=iFDD+ (tau=16)',
    #            'sensitivity-tau, FA=L2SPN (CX-Gnd-Goal, OR), FL=iFDD+ (tau=3)',
    #        ]
    #    }
    #
    #    'reorder_by_legend': [
    #        'FA=N, FL=iFDD+ (zeta=1)',
    #        'FA=N, FL=iFDD+ (zeta=3)',
    #        'FA=N, FL=iFDD+ (zeta=10)',
    #        ['FA=L2SPN', 'FL=iFDD+ (zeta=1)'],
    #        ['FA=L2SPN', 'FL=iFDD+ (zeta=3)'],
    #        ['FA=L2SPN', 'FL=iFDD+ (zeta=10)'],
    #    ],
    'reorder_by_legend': None,
    'add_analysis_with_no_matching_legend': False,      # used with reorder_by_legend, if True, plot grouped_analysis with legend that is not in reorder_by_legend
    # superceded by reorder_by_legend, use reorder_plots to match legend style with a grouped analysis
    # to know legend style for each #, run asyT.generate_all_legend_styles() in main function
    # set to value of -1 to skip a legend style
    'reorder_plots': False,
    # save figure settings
    'figsize': (8, 4),
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
    'mode': [],
    'remove_outlier': [0, 0]                            # [num of argmin, num of argmax] to remove, otherwise use a num which is equivalent to [num, num]
}

RPG_SUFFIX = { 'per_repetition': 'RPR', 'per_episode': 'RPE'}

# for benchmarking against PROST
PROST_IPPC2014 = {
    'academic_advising_inst_mdp__1': {'raw_score': -40.4, 'min_score': -59, 'max_score': -24},
    'academic_advising_inst_mdp__2': {'raw_score': -45.53, 'min_score': -72, 'max_score': -28},
    'academic_advising_inst_mdp__3': {'raw_score': -43.33, 'min_score': -80, 'max_score': -30},
    'academic_advising_inst_mdp__4': {'raw_score': -187.63, 'min_score': -220, 'max_score': -79},
    'academic_advising_inst_mdp__5': {'raw_score': -204.77, 'min_score': -216, 'max_score': -175},
    'academic_advising_inst_mdp__6': {'raw_score': -201.83, 'min_score': -212, 'max_score': -156},
    'academic_advising_inst_mdp__7': {'raw_score': -206.13, 'min_score': -217, 'max_score': -203},
    'academic_advising_inst_mdp__8': {'raw_score': -201.03, 'min_score': -223, 'max_score': -108},
    'academic_advising_inst_mdp__9': {'raw_score': -204.3, 'min_score': -221, 'max_score': -202},
    'academic_advising_inst_mdp__10': {'raw_score': -213.37, 'min_score': -217, 'max_score': -208},
    'crossing_traffic_inst_mdp__1': {'raw_score': -4.23, 'min_score': -6, 'max_score': -4},
    'crossing_traffic_inst_mdp__2': {'raw_score': -5.13, 'min_score': -9, 'max_score': -4},
    'crossing_traffic_inst_mdp__3': {'raw_score': -6.63, 'min_score': -11, 'max_score': -5},
    'crossing_traffic_inst_mdp__4': {'raw_score': -10.33, 'min_score': -28, 'max_score': -5},
    'crossing_traffic_inst_mdp__5': {'raw_score': -6.87, 'min_score': -10, 'max_score': -6},
    'crossing_traffic_inst_mdp__6': {'raw_score': -10.03, 'min_score': -40, 'max_score': -6},
    'crossing_traffic_inst_mdp__7': {'raw_score': -9.73, 'min_score': -19, 'max_score': -7},
    'crossing_traffic_inst_mdp__8': {'raw_score': -24.13, 'min_score': -40, 'max_score': -7},
    'crossing_traffic_inst_mdp__9': {'raw_score': -8.4, 'min_score': -11, 'max_score': -8},
    'crossing_traffic_inst_mdp__10': {'raw_score': -17.1, 'min_score': -40, 'max_score': -8},
    'elevators_inst_mdp__1': {'raw_score': -37.92, 'min_score': -60.5, 'max_score': -10.5},
    'elevators_inst_mdp__2': {'raw_score': -18.82, 'min_score': -39, 'max_score': -7.5},
    'elevators_inst_mdp__3': {'raw_score': -57.93, 'min_score': -79.5, 'max_score': -43.5},
    'elevators_inst_mdp__4': {'raw_score': -51.48, 'min_score': -84, 'max_score': -8.75},
    'elevators_inst_mdp__5': {'raw_score': -49.65, 'min_score': -70.5, 'max_score': -14.5},
    'elevators_inst_mdp__6': {'raw_score': -69.32, 'min_score': -104, 'max_score': -33.75},
    'elevators_inst_mdp__7': {'raw_score': -80.96, 'min_score': -123, 'max_score': -28.75},
    'elevators_inst_mdp__8': {'raw_score': -69.42, 'min_score': -122.75, 'max_score': -30.5},
    'elevators_inst_mdp__9': {'raw_score': -86.1, 'min_score': -168, 'max_score': -49.75},
    'elevators_inst_mdp__10': {'raw_score': -58.85, 'min_score': -132.5, 'max_score': -6.25},
    'skill_teaching_inst_mdp__1': {'raw_score': 70.67, 'min_score': 60.37, 'max_score': 72.49},
    'skill_teaching_inst_mdp__2': {'raw_score': 82.95, 'min_score': 71.65, 'max_score': 86},
    'skill_teaching_inst_mdp__3': {'raw_score': 96.27, 'min_score': -68.87, 'max_score': 175.08},
    'skill_teaching_inst_mdp__4': {'raw_score': 133.1, 'min_score': -4.61, 'max_score': 182.09},
    'skill_teaching_inst_mdp__5': {'raw_score': 74.83, 'min_score': -74.37, 'max_score': 156.57},
    'skill_teaching_inst_mdp__6': {'raw_score': -1.93, 'min_score': -334.6, 'max_score': 237.16},
    'skill_teaching_inst_mdp__7': {'raw_score': -63.62, 'min_score': -333.69, 'max_score': 218.42},
    'skill_teaching_inst_mdp__8': {'raw_score': -193.36, 'min_score': -478, 'max_score': 141.3},
    'skill_teaching_inst_mdp__9': {'raw_score': -168.04, 'min_score': -462.62, 'max_score': 122.05},
    'skill_teaching_inst_mdp__10': {'raw_score': -170.16, 'min_score': -603.69, 'max_score': 149.34},
    'tamarisk_inst_mdp__1': {'raw_score': -124.86, 'min_score': -241.59, 'max_score': -53.03},
    'tamarisk_inst_mdp__2': {'raw_score': -541.78, 'min_score': -753.92, 'max_score': -317.16},
    'tamarisk_inst_mdp__3': {'raw_score': -248.72, 'min_score': -664.48, 'max_score': -69.6},
    'tamarisk_inst_mdp__4': {'raw_score': -812.19, 'min_score': -1097.11, 'max_score': -443.14},
    'tamarisk_inst_mdp__5': {'raw_score': -738.79, 'min_score': -1109.07, 'max_score': -393.63},
    'tamarisk_inst_mdp__6': {'raw_score': -1010.16, 'min_score': -1200.36, 'max_score': -479.03},
    'tamarisk_inst_mdp__7': {'raw_score': -918.16, 'min_score': -1285.86, 'max_score': -463.09},
    'tamarisk_inst_mdp__8': {'raw_score': -1257.26, 'min_score': -1479.61, 'max_score': -943.86},
    'tamarisk_inst_mdp__9': {'raw_score': -923.06, 'min_score': -1383.86, 'max_score': -330.89},
    'tamarisk_inst_mdp__10': {'raw_score': -1420.94, 'min_score': -1691.36, 'max_score': -1000.36},
    'traffic_inst_mdp__1': {'raw_score': -4, 'min_score': -10, 'max_score': 0},
    'traffic_inst_mdp__2': {'raw_score': -11.7, 'min_score': -22, 'max_score': -6},
    'traffic_inst_mdp__3': {'raw_score': -11.97, 'min_score': -30, 'max_score': -1},
    'traffic_inst_mdp__4': {'raw_score': -42.23, 'min_score': -68, 'max_score': -6},
    'traffic_inst_mdp__5': {'raw_score': -49.23, 'min_score': -94, 'max_score': -30},
    'traffic_inst_mdp__6': {'raw_score': -63.13, 'min_score': -132, 'max_score': -37},
    'traffic_inst_mdp__7': {'raw_score': -44.9, 'min_score': -67, 'max_score': -33},
    'traffic_inst_mdp__8': {'raw_score': -47.93, 'min_score': -106, 'max_score': -8},
    'traffic_inst_mdp__9': {'raw_score': -20.43, 'min_score': -67, 'max_score': -9},
    'traffic_inst_mdp__10': {'raw_score': -129.97, 'min_score': -190, 'max_score': -81},
    'triangle_tireworld_inst_mdp__1': {'raw_score': 93.7, 'min_score': 90, 'max_score': 96},
    'triangle_tireworld_inst_mdp__2': {'raw_score': 94.23, 'min_score': 90, 'max_score': 96},
    'triangle_tireworld_inst_mdp__3': {'raw_score': 76.97, 'min_score': 70, 'max_score': 86},
    'triangle_tireworld_inst_mdp__4': {'raw_score': 76.73, 'min_score': 68, 'max_score': 85},
    'triangle_tireworld_inst_mdp__5': {'raw_score': 70.93, 'min_score': 63, 'max_score': 80},
    'triangle_tireworld_inst_mdp__6': {'raw_score': 72.4, 'min_score': 66, 'max_score': 80},
    'triangle_tireworld_inst_mdp__7': {'raw_score': -1.57, 'min_score': -40, 'max_score': 70},
    'triangle_tireworld_inst_mdp__8': {'raw_score': 30.13, 'min_score': -40, 'max_score': 70},
    'triangle_tireworld_inst_mdp__9': {'raw_score': -40, 'min_score': -40, 'max_score': -40},
    'triangle_tireworld_inst_mdp__10': {'raw_score': -40, 'min_score': -40, 'max_score': -40},
    'wildfire_inst_mdp__1': {'raw_score': -607.67, 'min_score': -4855, 'max_score': -40},
    'wildfire_inst_mdp__2': {'raw_score': -10162, 'min_score': -15325, 'max_score': -8065},
    'wildfire_inst_mdp__3': {'raw_score': -1263, 'min_score': -11250, 'max_score': -85},
    'wildfire_inst_mdp__4': {'raw_score': -18259.33, 'min_score': -27440, 'max_score': -4110},
    'wildfire_inst_mdp__5': {'raw_score': -3648, 'min_score': -12355, 'max_score': -85},
    'wildfire_inst_mdp__6': {'raw_score': -20457.33, 'min_score': -32000, 'max_score': -6730},
    'wildfire_inst_mdp__7': {'raw_score': -6126.83, 'min_score': -12305, 'max_score': -4180},
    'wildfire_inst_mdp__8': {'raw_score': -15396.17, 'min_score': -32790, 'max_score': -8190},
    'wildfire_inst_mdp__9': {'raw_score': -11876, 'min_score': -19755, 'max_score': -295},
    'wildfire_inst_mdp__10': {'raw_score': -19638.17, 'min_score': -28615, 'max_score': -13280}
}



def init_cycler(linestyles):
    # cycle different linecolors & linestyles to avoid lines of the same look
    colormap = 'combine'
    # colormap = 'tab10'
    # colormap = 'tab20'
    if colormap == 'combine':
        NUM_COLORS = 10
        cm = plt.get_cmap('tab10')
        linecolors = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
        NUM_COLORS = 8
        cm = plt.get_cmap('Accent')
        linecolors2 = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
        # linecolors2.reverse()
        linecolors2[1] = (0, 0, 0, 1)   # change to black cause original colour is too light
        linecolors += linecolors2
    elif colormap == 'tab10':
        NUM_COLORS = 10
        cm = plt.get_cmap(colormap)
        linecolors = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
    elif colormap == 'tab20':
        # use this to manually switch colours
        # tab20 is dark blue, light blue, dark orange, light orange, ...
        # we want dark blue, dark orange, ..., light blue, light orange, ...
        NUM_COLORS = 20
        cm = plt.get_cmap(colormap)
        linecolors = [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)]
        linecolors = [linecolors[0]] + [linecolors[2]] + [linecolors[4]] + [linecolors[6]] + [linecolors[8]] + [linecolors[10]] + [linecolors[12]] + [linecolors[14]] + [linecolors[16]] + [linecolors[18]] + [linecolors[1]] + [linecolors[3]] + [linecolors[5]] + [linecolors[7]] + [linecolors[9]] + [linecolors[11]] + [linecolors[13]] + [linecolors[15]] + [linecolors[17]] + [linecolors[19]]
    else:
        raise Exception('Invalid colormap specified')
    NUM_COLORS = len(linecolors)
    linecolors *= len(linestyles)
    # linestyles.reverse()
    linestyles *= NUM_COLORS
    default_cycler = (cycler(color=linecolors)              # cycle over different linecolors
                      + cycler(linestyle=linestyles)        # cycle over different linestyles
                      #+ cycler(lw=[1, 2, 3, 4])            # cycle over different linewidths
                     )
    plt.rc('axes', prop_cycle=default_cycler)



def save_legend_as_figure(legend, filename, expand = [-0, -0, 0, 0]):
    if legend == None:
        print('No legend is given')
        return
    legend.get_frame().set_linewidth(0.0)
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)


init_cycler(def_plot_settings['linestyles'])
plt.rcParams.update({'font.size': def_plot_settings['fontsize']})



def get_common_data(list_of_data, **kwargs):
    common_data = []
    for data in list_of_data:
        if same_dict(kwargs, data.get_attributes(), kwargs['identifier']):
            common_data.append( (data, dict2string(data.get_attributes())) )
    # v[1] is just a string description of data which is used to sort
    # the list of data into alphabetic order
    # this ordering is important to ensure consistent colour line plots for all figures
    common_data.sort(key = lambda v : v[1])
    return [data[0] for data in common_data]



class Analysis:    
    def __init__(self, logfile = None):
        self.attributes = {}
        self.actions = []
        self.states = []
        self.initial_state = []
        self.algorithm = None
        self.transitions = []
        self.total_episodes = 0
        self.max_steps = 0
        self.total_reward = []
        self.time_taken = []
        self.episodes = []                      # if episodes are not incremented by 1, this is a vector of episodes (e.g. [10, 20, 30])
        self.is_multi_tasks = False
        self.num_sessions = None
        self.num_episodes = None
        self.num_steps = None
        self.set_attribute('logfile', logfile)
        if logfile:
            self.set_attribute('logfolder', logfile[:logfile.rfind(os.sep)])
            logfile_ = os.path.normpath(logfile).split(os.sep)
            # use subfolder as logfolderID (this may not be sufficient so we do correction in grouped analysis)
            # Example: 2 folders with folderA/subfolderB and folderC/subfolderB will have the same logfolderID despite having different paths
            folder = logfile_[-4:-3]
            self.set_attribute('logfolderID', list2string(lsof_strings=folder, sort = False, linebreak = False, delimiter='_'))
        else:
            self.set_attribute('logfolder', None)
            self.set_attribute('logfolderID', None)
        
    def set_attribute(self, key, value, inst_id = None):
        if inst_id:
            if key in self.attributes:
                self.attributes[key][inst_id-1] = value
            else:
                self.attributes[key][inst_id-1] = [value]
        else:
            if key in self.attributes:
                self.attributes[key].append(value)
                if not self.is_multi_tasks and key.lower() == 'instance':
                    value0 = self.attributes.get(key, None)
                    if value != value0:
                        self.is_multi_tasks = True
            else:
                self.attributes[key] = [value]

    def delete_attribute(self, key):
        self.attributes.pop(key, None)

    def set_algorithm_type(self, line):
        if self.algorithm is None:   # analysis.algorithm is not None if there are two planners used, just consider the first planner which will be either UCT or PROST
            self.algorithm = absT.Algorithm_Type(line)
        else:
            algorithm = absT.Algorithm_Type(line)
            if algorithm.get_param('planner') not in self.algorithm.get_param('planners'):
                self.algorithm.params['planners'].append(algorithm.get_param('planner'))
                self.algorithm.params['planner'] = ''
                for planner in self.algorithm.get_param('planners'):
                    if self.algorithm.params['planner'] != '':
                        self.algorithm.params['planner'] += '+'
                    self.algorithm.params['planner'] += planner
    
    def set_lsof_actions(self, file):
        self.actions.append(absT.Actions(file))
    
    def set_lsof_states(self, file):
        self.states.append(absT.State(file))
    
    def get_attribute(self, key, inst_id = None):       # inst_id is required if running multi-instances in a single experiment
        if key == 'domain':
            return self.attributes.get(key, [''])[0]
        elif inst_id == None:
            return self.attributes.get(key, None)
        else:
            values = self.attributes.get(key, None)
            if values == None:
                return values
            else:
                return values[inst_id-1]
    
    def get_numeric_attribute(self, key, inst_id = None):  # inst_id is required if running multi-instances in a single experiment
        if key == 'domain':
            return self.attributes.get(key, [0])[0]
        elif inst_id == None:
            return self.attributes.get(key, 0)
        else:
            values = self.attributes.get(key, 0)
            if values == None:
                return 0
            elif values[inst_id-1]:
                return values[inst_id-1]
            else:
              return 0

    def get_attributes(self):
        kwargs = {}

        kwargs['logfolderID'] = self.get_attribute('logfolderID')
        kwargs['domain'] = self.get_attribute('domain')
        kwargs['num_sessions'] = self.num_sessions
        kwargs['num_episodes'] = self.num_episodes
        kwargs['episodes'] = self.episodes
        kwargs['num_steps'] = self.num_steps
        kwargs['parser'] = self.get_attribute('parser')
        kwargs['is_multi_tasks'] = self.is_multi_tasks
        kwargs['logfolder'] = self.get_attribute('logfolder')
        kwargs['instance'] = self.get_attribute('instance')
        kwargs['planner'] = self.algorithm.get_param('planner')
        kwargs['planners'] = self.algorithm.get_param('planners')
        kwargs['policy'] = self.algorithm.get_param('policy')

        kwargs['alpha'] = self.get_attribute('alpha')
        kwargs['batch'] = self.get_attribute('batch')
        kwargs['decay'] = self.get_attribute('decay')
        kwargs['epsilon'] = self.get_attribute('epsilon')
        if self.get_attribute('intrinsic_reward'):
            	kwargs['import_intrinsic_reward'] = self.get_attribute('import_intrinsic_reward')
        else:
            	kwargs['import_intrinsic_reward'] = None
        kwargs['import_qvalue'] = self.get_attribute('import_qvalue')
        kwargs['lambda'] = self.get_attribute('lambda')
        kwargs['horizon'] = self.get_attribute('horizon')

        kwargs['discount_factor'] = self.algorithm.get_param('discount_factor')
        kwargs['learner'] = self.get_attribute('learner')
        kwargs['learn_from_failure'] = self.get_attribute('learn_from_failure')
        kwargs['model_representation'] = self.get_attribute('model_representation')
        kwargs['experience'] = self.get_attribute('experience')
        kwargs['function_approximation'] = self.get_attribute('function_approximation')
        kwargs['function_approximation_feature_selection'] = self.get_attribute('function_approximation_feature_selection')
        kwargs['function_approximation_feature_selection_mod'] = self.get_attribute('function_approximation_feature_selection_mod')
        kwargs['function_approximation_context'] = self.get_attribute('function_approximation_context')
        kwargs['function_approximation_max_criteria'] = self.get_attribute('function_approximation_max_criteria')
        kwargs['features_learner'] = self.get_attribute('features_learner')
        kwargs['features_learner_sync_learning'] = self.get_attribute('features_learner_sync_learning')
        kwargs['features_learner_zeta'] = self.get_attribute('features_learner_zeta')
        kwargs['features_learner_initial_feature_size'] = self.get_attribute('features_learner_initial_feature_size')
        kwargs['features_learner_max_feature_size'] = self.get_attribute('features_learner_max_feature_size')
        kwargs['features_learner_tau'] = self.get_attribute('features_learner_tau')
        kwargs['eligibility_trace_type'] = self.get_attribute('eligibility_trace_type')
        kwargs['parser'] = self.get_attribute('parser')
        kwargs['initial_domain'] = self.get_attribute('initial_domain')
        kwargs['latent_objects'] = self.get_attribute('latent_objects')
        kwargs['dynamic_constraints'] = self.get_attribute('dynamic_constraints')
        kwargs['loop_detection'] = self.get_attribute('loop_detection')
        kwargs['replay_trajectory_to_goal'] = self.get_attribute('replay_trajectory_to_goal')
        kwargs['revert_to_best_policy'] = self.get_attribute('revert_to_best_policy')
        kwargs['beam_search_branch'] = self.get_attribute('beam_search_branch')
        kwargs['multi_planning'] = self.get_attribute('multi_planning')
        kwargs['num_hypothesis_domains'] = self.get_attribute('num_hypothesis_domains')
        kwargs['rollout_horizon'] = self.get_attribute('rollout_horizon')
        kwargs['max_round_for_ml'] = self.get_attribute('max_round_for_ml')
        kwargs['local_min_detection'] = self.get_attribute('local_min_detection')
        kwargs['intrinsic_reward'] = self.get_attribute('intrinsic_reward')
        kwargs['intrinsic_reward_rmax'] = self.get_attribute('intrinsic_reward_rmax')
        kwargs['intrinsic_reward_beta'] = self.get_attribute('intrinsic_reward_beta')
        kwargs['intrinsic_reward_beta_decay'] = self.get_attribute('intrinsic_reward_beta_decay')
        # kwargs['intrinsic_reward_experience'] = self.get_attribute('intrinsic_reward_experience')
        kwargs['intrinsic_reward_aggregation'] = self.get_attribute('intrinsic_reward_aggregation')
        kwargs['self_play'] = self.get_attribute('self_play')
        kwargs['mve_horizon'] = self.get_attribute('mve_horizon')
        kwargs['mqte_horizon'] = self.get_attribute('mqte_horizon')
        for key, item in kwargs.items():
            if isinstance(kwargs[key], list) and len(kwargs[key]) == 1:
                kwargs[key] = kwargs[key][0]
        for key in grouping_keys:
            if key not in kwargs:
                print("Key " + key + " is not being returned by Analysis.get_attributes(). This will cause error in grouping analyses")
        return kwargs

    # find attributes that are common in all analyses, then use it as the title
    def get_title(self, shorten = False):
        title = []
        use_domain_in_title = True
        for key in title_keys:
            if shorten and key not in shorten_title_keys:
                continue
            if key == 'domain' and not use_domain_in_title:
                continue
            attribute = self.get_attribute(key)
            if attribute == 'None' or attribute == None:
                # print("Can't find attribute " + key + " - omit from title")
                continue
            title.append(attribute)
        return list2string(lsof_strings=title, sort=False, linebreak=True, delimiter=' ') 
    
    def parse_state(self, file, only_one_state, line = None):
#        ----------Initial State---------------
#
#goal-reward-received: 0
#hasspare: 0
#spare-in(la2a1): 1
#spare-in(la2a2): 1
#spare-in(la3a1): 1
#vehicle-at(la1a1): 1
#vehicle-at(la1a2): 0
#vehicle-at(la1a3): 0
#vehicle-at(la2a1): 0
#vehicle-at(la2a2): 0
#vehicle-at(la3a1): 0
#
#not-flattire: 1
#Remaining Steps: 40
#StateHashKey: 2108
#
#Hashing of States is possible.
#Hashing of KleeneStates is possible.
#Both a goal and a dead end were found in the training phase.
#This task contains unreasonable actions.
#The final reward is determined by applying NOOP.
        # handle compact state printing
        phrase = "Current state:"
        if line != None and len(line.strip()) > len(phrase):
            # compare state printed
            if phrase in line:
                return self.states.get_simplestate(None, \
                          line[line.find(phrase)+len(phrase):].strip().replace(" |", "").split(" "))
            
        fluents = []
        values = []
        tmp_values = []
        for line in file:
            if "***********************************************" in line:
                break
            elif only_one_state and \
                ("Remaining Steps" in line \
                 or "StateHashKey" in line \
                 or  "Applicable actions" in line):
                break  # only works if printing state verbose
            elif ":" in line and \
                    "Remaining Steps" not in line \
                    and "StateHashKey" not in line \
                    and "Applicable actions" not in line:
                fluent = line[:line.find(":")].rstrip()
                try:
                    self.states[-1].get_index(fluent)
                except:
                    fluents = []
                    break   # unrecognizable fluent, assume that no fluents are printed in logfile
                fluents.append(fluent)
                values.append(line[line.find(":")+2:].rstrip())
            else:
                if not tmp_values:
                    tmp_values = line.strip().split(" ")
        if values == []:
            fluents = None
            values = tmp_values
        if values == [] or fluents == []:
            raise Exception("Error in parsing state for logfile: " + self.logfile)
        return self.states[-1].get_simplestate(fluents, values)
       
    def parse_precond(self, file):
        #---------Action Preconditions---------
        #
        #Precond 0
        #  HashIndex: 8, deterministic, caching in vectors, Kleene caching in vectors of size 54.
        #
        #  Action Hash Key Map: 
        #    move(r1, wp0, wp0)  : 1
        #  Formula: 
        #(or (not move(r1, wp0, wp0))  (and robot_at(r1, wp0) localised(r1) undocked(r1)) ) 
        #
        #
        #--------------
        #Precond 1
        #  HashIndex: 9, deterministic, caching in vectors, Kleene caching in vectors of size 54.
        #
        #  Action Hash Key Map: 
        #    move(r1, wp0, wp1)  : 1
        #  Formula: 
        #(or (not move(r1, wp0, wp1))  (and robot_at(r1, wp0) localised(r1) undocked(r1)) ) 
        #
        #
        #--------------
        phrase1 = "Precond"
        phrase2 = "Action Hash Key Map:"
        phrase3 = "Formula:"
        parse_action_next = False
        parse_formula_next = False
        for line in file:
            if "----------Initial State---------------" in line:
                break
            elif phrase1 in line:
                precond_index = int(line[len(phrase1):].strip())
            elif phrase2 in line:
                parse_action_next = True
            elif parse_action_next:
                action_name = line[:-4].strip()
                parse_action_next = False
            elif phrase3 in line:
                parse_formula_next = True
            elif parse_formula_next:
                precond = line.strip()
                parse_formula_next = False
                self.actions.set_action_precond(action_name, precond_index, precond)
        
    def set_initial_state(self, file):
        self.initial_state.append(self.parse_state(file, True))
        
    def parse_counter(self, line):
        phrase1 = "Planning step "
        phrase2 = "round "
        phrase3 = "episode "
        pos1 = line.find(phrase1)
        pos2 = line.find("/", pos1)
        step_id = int(line[pos1+len(phrase1) : pos2])
        pos1 = line.find(phrase2)
        pos2 = line.find("/", pos1)
        round_id = int(line[pos1+len(phrase2) : pos2])
        pos1 = line.find(phrase3)
        pos2 = line.find(")", pos1)
        episode_id = int(line[pos1+len(phrase3) : pos2])
        return (episode_id, round_id, step_id)
       
    def parse_action_taken(self, line):
        phrase = "Submitted action: "
        pos1 = line.find(phrase)
        pos2 = line.find(")")
        if pos2 > pos1:
            fluent = line[pos1 + len(phrase) : pos2+1].strip()
        else:
            fluent = line[pos1 + len(phrase) :].replace(":", "").strip()
        index = self.actions[-1].get_index(fluent)
        if index == None:
            raise Exception("Action fluent " + fluent + " does not exist")            
        return absT.SimpleAction(index, fluent)
     
    def parse_execution_status(self, line):
        phrase = "Execution status: "
        if phrase not in line:
            return None
        else:
            # True if successfully executed
            return line[line.find(phrase) + len(phrase) :].strip() == "success"

    def parse_execution_statuses(self, file):
        phrase = "Round "
        status_matrix = []
        prev_round_num = 0
        for line in file:
            if phrase in line:
                pos = line.find(":")
                round_num = int(line[len(phrase):pos].strip())
                prev_round_num = prev_round_num + 1
                assert(round_num == prev_round_num)
                status_matrix.append(line[pos+1:line.find('=')].strip().split(" "))
            else:
                break
        return status_matrix
    
    def parse_round_information(self, file):
        phrase = "Round"
        results = []
        for line in file:
            if phrase in line and '/' not in line:
                pos = line.find(":")
                result = line[pos+1:].strip().split(" ")
                result = [float(r) for r in result if r]
                results += result
            else:
                break
        return results

    def parse_reward_received(self, line):
        phrase = "Immediate reward: "
        return float(line[line.find(phrase) + len(phrase) :].rstrip())

    def parse_string_of_numbers(self, file):
        phrase = "Round "
        reward_matrix = []
        prev_round_num = 0
        for line in file:
            if phrase in line:
                pos1 = line.find(":")
                pos2 = line.find(" = ")
                round_num = int(line[len(phrase):pos1].strip())
                prev_round_num = prev_round_num + 1
                assert(round_num == prev_round_num)
                reward_matrix.append(line[pos1+1:pos2].strip().split(" "))
            else:
                break
        return reward_matrix
            
    def add_transition(self, pre_state, action, post_state, reward, original_reward, \
                       status, episode_id, round_id, step_id):
        self.transitions.append(absT.Transition(pre_state, \
                                                action, \
                                                post_state, \
                                                reward, \
                                                original_reward, \
                                                status, \
                                                episode_id, \
                                                round_id, \
                                                step_id))
        if self.total_episodes < episode_id:
            self.total_episodes = episode_id
        if self.max_steps < step_id:
            self.max_steps = step_id
    
    def set_episode_reward(self, line):
        phrase = "REWARD RECEIVED: "
        self.total_reward.append(float(line[line.find(phrase) + len(phrase):]))
        
    def set_time_taken(self, line):
        phrase = "Time taken for session"
        session_id = int(line[line.find(phrase)+len(phrase) : line.find(": ")])
        time_taken = float(line[line.find(": ")+2 : line.find("seconds")].strip())
        self.time_taken.append((session_id, time_taken))

    def get_initial_state(self, inst_id = None):
        if inst_id == None:
            return self.initial_state
        else:
            return self.initial_state[inst_id-1]

    # this takes a lot of memory, avoid this!
    def get_episode_step_matrix(self):
        matrix = np.zeros((self.total_episodes, self.max_steps))
        for transition in self.transitions:
             matrix[transition.episode_id-1][transition.step_id-1] = 1
        return matrix
        
    # an array with size = number of episodes, and each element has a value = num of steps
    def get_num_steps_per_episode(self):
        if self.num_steps:
            return self.num_steps           # return scalar to reduce memory usage
        else:
            return np.sum(self.get_episode_step_matrix(), axis = 1)
    
    # an array with size = number of steps, and each element has a value = num of episodes
    def get_num_episodes_per_step(self):
        if self.num_episodes:
            return self.num_episodes        # return scalar to reduce memory usage
        else:
            return np.sum(self.get_episode_step_matrix(), axis = 0)        
    
    def get_data(self, dataType, mode = None):
        result = None
        # if dataType == 'norm_rewards':
        #     return self.norm_rewards.get(mode)
        if dataType == 'original_rewards':
            result = self.original_rewards.get(mode)
        elif dataType == 'rewards':
            result = self.rewards.get(mode)
        elif dataType == 'original_rewards_per_round':
            result = self.original_rewards_per_round.get(mode)
        elif dataType == 'rewards_per_round':
            result = self.rewards_per_round.get(mode)
        # elif dataType == 'rewards_computation_time_per_round':
        #     result = self.rewards_computation_time_per_round.get(mode)
        elif dataType == 'succ_exec':
            result = self.succ_executions.get(mode)
        elif dataType == 'execution_timestamp':
            result = self.execution_timestamp.get(mode)
        elif dataType == 'computation_time_per_round':
            result = self.computation_time_per_round.get(mode)
        elif dataType == 'num_features_per_round':
            result = self.num_features_per_round.get(mode)
        elif dataType == 'time_taken':
            result = self.get_time_taken(False)
        elif dataType == 'terminal_state':
            result = self.terminal_states.get(mode)
        elif dataType == 'goal_state':
            terminal_states = self.terminal_states.get(mode)
            # if reach goal, then value = 1
            reach_goal = [1 if ts == 1 else 0 for ts in terminal_states[0]]
            result = (reach_goal, terminal_states[1])
        elif dataType == 'deadend_state':
            terminal_states = self.terminal_states.get(mode)
            # if reach deadend, then value = -1
            reach_deadend = [1 if ts == -1 else 0 for ts in terminal_states[0]]
            result = (reach_deadend, terminal_states[1])
        elif dataType == 'non_goal_state':
            terminal_states = self.terminal_states.get(mode)
            # if reach goal, then value = 1
            # thus, if value != 1, then not reach goal = 1
            not_reach_goal = [1 if ts != 1 else 0 for ts in terminal_states[0]]
            result = (not_reach_goal, terminal_states[1])
        else:
            raise Exception("No such data: " + dataType)
        if len(result) > 2:
            return result[:2]
        else:
            return result
    
    def get_time_taken(self, average = False):
        if average:
            time_taken = [t for session_id, t in self.time_taken]
            return sum(time_taken)/len(time_taken)
        else:
            time_taken = [0]*len(self.time_taken)
            for session_id, t in self.time_taken:
                time_taken[session_id-1] = t
            return time_taken

    def finish(self, rewards_received = [], \
                     original_rewards_received = [], \
                     execution_statuses = [], \
                     execution_timestamp = [], \
                     terminal_states_per_round = [], \
                     computation_time_per_round = [], \
                     num_features_per_round = [],
                     episodes = []):

        # DEPRECATED to reduce memory consumption
        # if not self.transitions:
        #     # need to reconstruct data from matrices rewards_received & execution_statuses
        #     if not rewards_received:
        #         raise Exception("Incomplete log info!")
        #     elif len(rewards_received) != len(execution_statuses):
        #         raise Exception("Sizes of rewards_received (" + str(len(rewards_received)) + 
        #                         ") and execution_statuses (" + str(len(execution_statuses)) + ") should be the same!")
            
        #     episode_id = 0
        #     for lsof_rewards, lsof_original_rewards, lsof_statuses in zip(rewards_received, original_rewards_received, execution_statuses):
        #         round_id = 0
        #         for rewards, original_rewards, statuses in zip(lsof_rewards, lsof_original_rewards, lsof_statuses):
        #             round_id = round_id+1
        #             episode_id = episode_id+1
        #             step_id = 0
        #             for reward, original_reward, status in zip(rewards, original_rewards, statuses):
        #                 step_id = step_id+1
        #                 self.add_transition(None, None, None, \
        #                                     float(reward), float(original_reward), status == "1", \
        #                                     episode_id, round_id, step_id)
        
        self.num_sessions, self.num_episodes, self.num_steps = np.shape(rewards_received)
        if episodes:
            self.episodes = episodes
            self.num_episodes = int(max(episodes))
        # rmax = self.get_attribute('rmax', 1)
        # if rmax:
        #     rmax = abs(rmax)
        # else:
        #     rmax = 1
        num_episodes_per_step = self.get_num_episodes_per_step() * self.num_sessions
        num_steps_per_episode = self.get_num_steps_per_episode()
        if self.episodes:
            rewards = np.zeros((len(self.episodes), num_steps_per_episode))
            original_rewards = np.zeros((len(self.episodes), num_steps_per_episode))
            # norm_rewards = np.zeros((len(self.episodes), num_steps_per_episode))
            succ_executions = np.zeros((len(self.episodes), num_steps_per_episode))
        elif np.isscalar(num_episodes_per_step) and np.isscalar(num_steps_per_episode):
            rewards = np.zeros((num_episodes_per_step, num_steps_per_episode))
            original_rewards = np.zeros((num_episodes_per_step, num_steps_per_episode))
            # norm_rewards = np.zeros((num_episodes_per_step, num_steps_per_episode))
            succ_executions = np.zeros((num_episodes_per_step, num_steps_per_episode))
        else:
            rewards = np.zeros( (int(num_episodes_per_step.max()), np.size(num_episodes_per_step)))
            original_rewards = np.zeros( (int(num_episodes_per_step.max()), np.size(num_episodes_per_step)))
            # norm_rewards = np.zeros( (int(num_episodes_per_step.max()), np.size(num_episodes_per_step)))
            succ_executions = np.zeros( (int(num_episodes_per_step.max()), np.size(num_episodes_per_step)))
        
        if self.transitions:                                                                # DEPERECATED
            for transition in self.transitions:
                # each row represents the results of steps within a episode
                # each column represents another episode
                rewards[transition.episode_id-1][transition.step_id-1] = transition.reward
                original_rewards[transition.episode_id-1][transition.step_id-1] = transition.original_reward
                # norm_rewards[transition.episode_id-1][transition.step_id-1] = transition.reward / rmax
                succ_executions[transition.episode_id-1][transition.step_id-1] = 1 if transition.executed else 0
        else:
            episode_id = 0
            for lsof_rewards, lsof_original_rewards, lsof_statuses in zip(rewards_received, original_rewards_received, execution_statuses):     # loop over each session
                for rewards_, original_rewards_, statuses_ in zip(lsof_rewards, lsof_original_rewards, lsof_statuses):                          # loop over each episode in a session
                    episode_id = episode_id+1
                    step_id = 0
                    for reward_, original_reward_, status_ in zip(rewards_, original_rewards_, statuses_):                                      # loop over each step in an episode
                        step_id = step_id+1
                        rewards[episode_id-1][step_id-1] = float(reward_)
                        # if rewards[episode_id-1][step_id-1] < 0:                          # ignore action cost
                        #   rewards[episode_id-1][step_id-1] = 0
                        # add action cost when reached deadend else reaching deadend might be better than not reaching it when there is action cost
                        if terminal_states_per_round[episode_id-1] == -1 and rewards[episode_id-1][step_id-1] == 0:
                            rewards[episode_id-1][step_id-1] = ACTION_COST
                        original_rewards[episode_id-1][step_id-1] = float(original_reward_)
                        # self.norm_rewards[episode_id-1][step_id-1] = float(reward) / rmax
                        succ_executions[episode_id-1][step_id-1] = 1 if status_ else 0
        
        # DEPERECATED to reduce memory usage
        # self.rewards = absT.DataMatrix('rewards', rewards, num_steps_per_episode, num_episodes_per_step)
        # self.original_rewards = absT.DataMatrix('orignal_rewards', original_rewards, num_steps_per_episode, num_episodes_per_step)
        # self.norm_rewards = absT.DataMatrix('norm_rewards', norm_rewards, num_steps_per_episode, get_num_episodes_per_step)
        rewards_per_round = np.sum(rewards, axis = 1)
        self.rewards_per_round = absT.DataMatrix('rewards_per_round', rewards_per_round, num_steps_per_episode, num_episodes_per_step, episodes)
        self.original_rewards_per_round = absT.DataMatrix('original_rewards_per_round', np.sum(original_rewards, axis = 1), num_steps_per_episode, num_episodes_per_step, episodes)
        self.succ_executions = absT.DataMatrix('succ_exec', succ_executions, num_steps_per_episode, num_episodes_per_step, episodes)
        self.terminal_states = absT.DataMatrix('terminal_state', terminal_states_per_round, num_steps_per_episode, num_episodes_per_step, episodes)
        self.execution_timestamp = absT.DataMatrix('execution_timestamp', execution_timestamp, num_steps_per_episode, num_episodes_per_step, episodes)
        self.computation_time_per_round = absT.DataMatrix('computation_time_per_round', computation_time_per_round, num_steps_per_episode, num_episodes_per_step, episodes)
        self.num_features_per_round = absT.DataMatrix('num_features_per_round', num_features_per_round, num_steps_per_episode, num_episodes_per_step, episodes)
        # this is wrong: if rewards < 0, then longer computation time gives better performance, doesn't make sense
        # self.rewards_computation_time_per_round = absT.DataMatrix('rewards_computation_time_per_round', np.divide(rewards_per_round, np.array(computation_time_per_round)), num_steps_per_episode, num_episodes_per_step)
        intrinsic_reward = self.get_attribute('intrinsic_reward')
        if not intrinsic_reward or all(['disabled' == v for v in intrinsic_reward]):
            self.delete_attribute('import_intrinsic_reward')
            self.set_attribute('import_intrinsic_reward', None)

        del num_episodes_per_step
        del num_steps_per_episode
        del rewards
        del original_rewards
        # del norm_rewards
        del succ_executions
        gc.collect()

    def print_attribute(self, key, inst_id = None):
        values = self.attributes.get(key, 'None')
        if inst_id != None:
            return values[inst_id-1]
        elif values == 'None':
            return values
        elif self.is_multi_tasks:
            string = ''
            for value in values:
                string = value + ', '
            return string[:-2]
        else:
            return values[0]   # all values are same

    def print_algorithm(self):
        return self.algorithm.print()

    def print_lsof_actions(self, inst_id = None):
        if inst_id != None:
            return self.actions[inst_id-1].print()
        elif self.is_multi_tasks:  
            string = ''
            for i in range(self.actions.len()):
                string = string + 'Instance ' + str(i) + \
                        '\n' + self.actions[i].print()
        else:
            return self.actions[0].print()   # all values are same

    def print_lsof_states(self, inst_id = None):
        if inst_id != None:
            return self.states[inst_id-1].print()
        elif self.is_multi_tasks:  
            string = ''
            for i in range(self.states.len()):
                string = string + 'Instance ' + str(i) + \
                        '\n' + self.states[i].print()
        else:
            return self.states[0].print()   # all values are same

    def print_initial_state(self, inst_id = None):
        if inst_id != None:
            return self.initial_state[inst_id-1].print()
        elif self.is_multi_tasks:  
            string = ''
            for i in range(self.initial_state.len()):
                string = string + 'Instance ' + str(i) + \
                        '\n' + self.initial_state[i].print()
        else:
            return self.initial_state[0].print()   # all values are same
        
    def print_transitions(self, episode_id = None, step_id = None):
        string = ""
        for transition in self.transitions:
            if episode_id == None or episode_id == transition.episode_id:
                if step_id == None or step_id == transition.step_id:
                    string += "Transition for Episode " + str(episode_id) + \
                          ", Step: " + str(step_id) + "\n"
                    string += transition.print() + "\n"
        return string

    def print_time_taken(self, average = False):
        if average:
            print("Average Time: " + str(self.get_time_taken(True)))
        else:
            for session_id, time_taken in self.time_taken:
                print("Session "+str(session_id)+": "+str(time_taken)+" seconds")

    def plot_data(self, dataType, **plot_settings):
        y, std_dev, episodes = self.get_data(dataType, plot_settings['mode'])
        if 'title' not in plot_settings or plot_settings['title'] == "undef":
            plot_settings['title'] = self.print_algorithm()
        return plot_data(episodes, y, std_dev, **plot_settings)


class MultiAnalysis:    
    def __init__(self, analyses, logfolder = None, identifier = None):
        self.plot_keys = plot_keys
        self.analyses = analyses
        self.identifier = identifier
        self.logfolder = logfolder
        set_logfolderID(self.analyses)

    def print_aggregated_analyses(self, grouped_analyses, **kwargs):
        grouped_analyses.sort(key = (absT.sortMatrices))
        if kwargs.get('reorder_plots', False):
            order = kwargs['reorder_plots']
        else:
            order = list(range(0, len(grouped_analyses)))
        for analysis_num in order:
            grouped_analysis = grouped_analyses[analysis_num]
            stacked_y, agg_y, std_dev, _ = grouped_analysis.get(mode = kwargs['mode'], remove_outlier = kwargs['remove_outlier'])
            kwargs['title'], legend_keys = self.get_title(grouped_analyses, exclude_legend_keys = kwargs.get('exclude_legend_keys', None))
            print(kwargs['title'])
            print(grouped_analysis.get_label(legend_keys))
            print(get_ylabel(kwargs['mode']))
            print('    Agg = ' + str(agg_y[-1]) + ', std-dev = ' + str(std_dev[-1]))
            kwargs['label'] = [logfolder[0][-4:] for logfolder in grouped_analysis.get_label('logfolder')]  # list of list of a single element which is the path of logfolder, extract last 4 chars
            for y, label in zip(stacked_y, kwargs['label']):
                print('        ' + label + ' = ' + str(y[-1]))


    def plot(self, delete_grouping_keys, argv, **kwargs):
        plot_settings = copy.deepcopy(def_plot_settings)
        plot_settings.update(kwargs)

        for arg in argv:   # argv is a list of lists, each list is a plot command
            mode = copy.deepcopy(arg)
            # rewards and original_rewards are DEPRECATED and replaced with rewards_per_round and original_rewards_per_round, respectively
            # this is to save memory and computation usage
            # if we want to plot avg rewards, then we need to enable rewards and original_rewards again
            if 'rewards' in mode and 'terminal' in mode:
                mode.remove('rewards')
                mode.remove('terminal')
                mode.append('rewards_per_round')
            if 'original_rewards' in mode and 'terminal' in mode:
                mode.remove('original_rewards')
                mode.remove('terminal')
                mode.append('original_rewards_per_round')

            kwargs = copy.deepcopy(plot_settings)
            if exclude_legend_keys:
                kwargs['exclude_legend_keys'] = exclude_legend_keys
            for key in self.plot_keys:
                kwargs[key] = key in arg
                if kwargs[key]:
                    mode.remove(key)
            # for arg_ in arg:
            #     if isinstance(arg_, list) and all([isinstance(a, str) for a in arg_]):
            #         kwargs['legend_labels'] = arg_
            #         break
            kwargs['mode'] = mode
            if kwargs['cross']:
                kwargs['mode'].append('cross')
            elif kwargs['agg']:
                kwargs['mode'].append('agg')
            elif kwargs['overlay']:
                kwargs['mode'].append('overlay')
            elif kwargs['value']:
                kwargs['mode'].append('value')

            if kwargs['cross'] or kwargs['agg'] or kwargs['overlay'] or kwargs['value']:
                # set identifier to all possible keys
                # essentially we are not grouping the data, just converting
                # list of Analysis to list of DataMatrix (grouped_data)
                if kwargs['is_rpg']:
                    # do not group by instance if using RPG
                    kwargs['identifier'] = [k for k in grouping_keys if k != 'instance' and k not in delete_grouping_keys]
                else:
                    kwargs['identifier'] = [k for k in grouping_keys if k not in delete_grouping_keys]
                grouped_data = self.get_grouped_data(self.analyses, **kwargs)
                if grouped_data is not None:                                    # grouped_data is None if data is computation time and hardware used are different
                    if kwargs['concatenate'] or kwargs['concatenate-agg']:
                        try:
                            common_grouped_data = []
                            cache = []
                            kwargs_copy = copy.deepcopy(kwargs)
                            for data in grouped_data:
                                # strip off the number '-0001', '-0002', etc. so that experiments from different parent folders are grouped separately
                                # E.g.: Separate parent1/results-0001/<domain>/experiment-0001/ and parent2/results-0001/<domain>/experiment-0001/
                                #       but group parent1/results-0001/<domain>/experiment-0001/ and parent1/results-0002/<domain>/experiment-0001/
                                data.set_attribute('logfolderID', data.get_attribute('logfolderID')[:-5])
                            for data in grouped_data:
                                kwargs_copy.update(data.get_attributes())
                                # check if data is in cache
                                if not dict_in_list_of_dict(cache, kwargs_copy, kwargs_copy['identifier']):
                                    # records data that has been grouped already, each analysis can only be in 1 group
                                    attributes = copy.deepcopy(data.get_attributes())
                                    cache.append(attributes)
                                    # extract data that have same identifier
                                    common_grouped_data.append(get_common_data(grouped_data, **kwargs_copy))
                            lsof_concatenate_data = []
                            for new_grouped_data in common_grouped_data:
                                concatenate_data = []
                                for rep_num in range(len(new_grouped_data[0].data)):    # loop over each experiment_..._000X folder
                                    stacked_y = []
                                    logfolders = []
                                    for log_id in range(len(new_grouped_data)):         # loop over each logfolder
                                        if len(new_grouped_data[log_id].data) != len(new_grouped_data[0].data):
                                            if rep_num == len(new_grouped_data[log_id].data):
                                                print('log_id #'+str(log_id)+' has mismatching number of logfolders = '+str(len(new_grouped_data[log_id].data)))
                                                print('    >> Folder: '+new_grouped_data[log_id].identifier['logfolder'][rep_num-1][0])
                                            continue
                                        stacked_y += new_grouped_data[log_id].data[rep_num].data.tolist()
                                        logfolders += [new_grouped_data[log_id].identifier['logfolder'][rep_num]]
                                    if stacked_y:
                                        episodes_per_step = len(stacked_y)
                                        stacked_y = np.array( [[y for y in stacked_y]] )
                                        identifier = copy.deepcopy(new_grouped_data[0].identifier)
                                        identifier['logfolder'] = logfolders
                                        identifier['logfolderID'] = logfolders[0][0]
                                        identifier['logfolderID'] = identifier['logfolderID'][identifier['logfolderID'].rfind('_')+1:]    # this will retain only the last 4 digits
                                        concatenate_data.append( \
                                            absT.DataMatrices(new_grouped_data[0].name, \
                                            stacked_y, \
                                            identifier, \
                                            new_grouped_data[0].data[0].steps_per_episode, \
                                            episodes_per_step,
                                            new_grouped_data[0].data[0].episodes))
                                if kwargs['concatenate-agg']:
                                    lsof_concatenate_data.append(absT.merge_DataMatrices(concatenate_data))
                                else:
                                    lsof_concatenate_data += concatenate_data
                            grouped_data = lsof_concatenate_data
                        except Exception as e:
                            print(e)
                            print('Fail to plot in concatenation')
                    
                    if kwargs['value']:
                        self.print_aggregated_analyses(grouped_data, **kwargs)
                    else:
                        # print('Plotting aggregated analysis')
                        self.plot_aggregated_analyses(grouped_data, **kwargs)
            else:
                # print('Plotting individual analysis')
                self.plot_individual_analysis(**kwargs)


    def plot_individual_analysis(self, **kwargs):
        # plot each experimental run by itself
        if kwargs['save'] and kwargs['show_fig']:
             # show after saving else a blank image will be saved
            show_fig = True
            kwargs['show_fig'] = False
        else:
            show_fig = False
        for analysis in self.analyses:
            dataType = get_data_type(kwargs['mode'])
            kwargs['label'] = analysis.get_attribute('logfolder')[0][-4:]
            if 'ax' in kwargs:
              kwargs['ax'] = None                           # so that analysis.plot_data will create a new figure
            kwargs = analysis.plot_data(dataType, **kwargs)
            if kwargs['save']:
                title = analysis.get_title(True)
                filename = title.replace('\n','_').replace(' ','_').replace(':', '-') + \
                            "_" + list2string(lsof_strings=kwargs['mode'], sort=True, linebreak=False, delimiter='__') + \
                            "." + kwargs['format']
                folder = self.logfolder
                if not os.path.isdir(folder):
                    os.makedirs(folder)
                kwargs['fig'].set_size_inches(kwargs['figsize'][0], kwargs['figsize'][1])
                filename = filename[: filename.rfind('.')] + '__' + gen_num(folder, filename[: filename.rfind('.')]) + filename[filename.rfind('.') :]
                # if use bbox_inches, this will prevent figure from cropping off stuff, however, title wrap no longer works
                plt.savefig(os.path.join(folder, filename), format=kwargs['format'], bbox_inches="tight", dpi=kwargs['dpi'])
                # plt.savefig(folder+filename, format=kwargs['format'], dpi=kwargs['dpi'])
                plt.close(plt.gcf())          # save memory by closing current figure
            if show_fig:
                plt.show()
        plt.close()
                        
    # this assumes that grouped_analyses are sorted by their instances
    # as a new figure is created once the instance changes in the for...loop
    def plot_aggregated_analyses(self, grouped_analyses, **kwargs):
        # instance = None
        save_fig = kwargs['save']
        show_fig = kwargs['show_fig']
        ippc_folder = os.path.normpath(self.logfolder).split(os.sep)[:-2]
        kwargs['ippc_log'] = os.sep+os.path.join(*ippc_folder, 'ippc_scores.log')          # to save IPPC scores in this folder

        # DEPRECATED: this depends on self.identifier and may include additional common attributes
        # replaced with MultiAnalysis.get_title()
        # get identifiers that are not used to group analyses, these shall be displayed in legend
        # legend_keys = [k for k in grouping_keys if k not in self.identifier]

        count = 0
        fig_num = None
        legend_labels = ''
        dummy_y = 0
        folder = ''
        grouped_analyses.sort(key = (absT.sortMatrices))

        if kwargs.get('reorder_by_legend', False):
            non_matching_analyses = []                                                  # list of indices of grouped_analysis which have legends not in reorder_by_legend
            analysis_num = 0
            if isinstance(kwargs['reorder_by_legend'], dict):
                domain = grouped_analyses[0].get_attribute('domain')
                ordered_legends = kwargs['reorder_by_legend'].get(domain, [])
                if ordered_legends == []:
                    domain = domain.replace('_mdp', '')                                 # strip off _mdp from key and try again
                    ordered_legends = kwargs['reorder_by_legend'].get(domain, [])
                if ordered_legends == []:
                    ordered_legends = kwargs['reorder_by_legend'].get('default', [])
            else:
                ordered_legends = kwargs['reorder_by_legend']
            if ordered_legends == []:
              raise Exception('ordered_legends cannot be an empty list')
            order = [-1] * len(ordered_legends)                                         # initialise order with size = num of legends given, do dummy plot if no grouped_analysis has a matching legend

            for grouped_analysis in grouped_analyses:
                _, agg_y, _, _ = grouped_analysis.get(mode = kwargs['mode'], remove_outlier = kwargs['remove_outlier'])
                if np.size(agg_y) == 0:
                    continue
                dummy_y = agg_y[0]
                _, legend_keys = self.get_title(grouped_analyses, exclude_legend_keys = kwargs.get('exclude_legend_keys', None))
                grouped_legend = grouped_analysis.get_label(legend_keys)
                matching_label = []
                # this allows partial matching rather than exact match of legend keys
                for ordered_legend in ordered_legends:
                    if not isinstance(ordered_legend, list):
                        ordered_legend = [ordered_legend]
                    all_matches = True                                                  # all members in list must be in grouped_legend
                    for v in ordered_legend:
                        if v not in grouped_legend:
                            all_matches = False
                            break
                    if all_matches:
                        matching_label.append(len(ordered_legend))                      # append length of ordered_legend if it is a match
                    else:
                        matching_label.append(0)

                max_len = max(matching_label)                                           # = 0 if no match
                num_matches = matching_label.count(max_len) if max_len > 0 else 0       # if no match, then num_matches is zero, if more than one match, tiebreak is to use match which has the most elements in its list

                if num_matches == 1:
                    order_index = matching_label.index(max_len)                         # select match corresponding to ordered_legend with the largest length
                    order[order_index] = analysis_num
                    # print('Grouped analysis has legend \'' + grouped_analysis.get_label(legend_keys) + '\' which is in reorder_by_legend')
                elif num_matches == 0:
                    # no such legend in grouped_analyses, will do a dummy plot since order is initalize as list of -1
                    print('Grouped analysis has legend \'' + grouped_analysis.get_label(legend_keys) + '\' which is not in reorder_by_legend')
                    non_matching_analyses.append(analysis_num)
                else:
                    raise Exception('Grouped analysis has legend \'' + grouped_analysis.get_label(legend_keys) + '\' which has multiple matches in reorder_by_legend: ' + \
                         ''.join('T' if v else 'F' for i,v in enumerate(matching_label)))     # print T if matches with -th legend in kwargs['reorder_by_legend'], otherwise F
                    non_matching_analyses.append(analysis_num)
                analysis_num += 1
            if kwargs.get('add_analysis_with_no_matching_legend', True):
                order += non_matching_analyses
        elif kwargs.get('reorder_plots', False):
            # set the order of grouped analysis to plot, this is to ensure legends are consistent over different figures
            order = kwargs['reorder_plots']
        else:
            # order of grouped analysis follows the lexical order of folders numbering
            order = list(range(0, len(grouped_analyses)))

        for analysis_num in order:
            filename = ''
            if analysis_num >= 0:
                grouped_analysis = grouped_analyses[analysis_num]
                stacked_y, agg_y, std_dev, episodes = grouped_analysis.get(mode = kwargs['mode'], remove_outlier = kwargs['remove_outlier'])
                if isinstance(agg_y, (list, tuple, np.ndarray)) and np.size(agg_y) != 0:
                    dummy_y = agg_y[0]
            else:
                # producing dummy point to skip legend entry
                grouped_analysis = None
                stacked_y = dummy_y
                agg_y = dummy_y
                std_dev = None
                episodes = None
            if np.size(agg_y) == 0:
                continue
            if 'cross' in kwargs['mode']:                                                                     # check which mode should plot be overlayed
                kwargs['title'], legend_keys = self.get_title(grouped_analyses, exclude_legend_keys = kwargs.get('exclude_legend_keys', None))
                filename, _ = self.get_title(grouped_analyses, exclude_legend_keys = kwargs.get('exclude_legend_keys', None), shorten = True)
                if grouped_analysis == None:
                    kwargs['label'] = '#' + str(analysis_num)                                                 # dummy plot
                else:
                    kwargs['label'] = grouped_analysis.get_label(legend_keys)                                 # this is legend text
                    if kwargs['label']:
                        kwargs['label'] = '#' + str(analysis_num) + '~' + kwargs['label']                     # this is legend text
                kwargs['save'] = False
                kwargs['show_fig'] = False
                # check if instance has changed
                # this is not used because only analyses of the same instance
                # are in MuliAnalysis
#                if instance != None and \
#                    instance != grouped_analysis.get_attribute('instance'):
#                    if show_fig:
#                        kwargs['mfig'].show()
#                    kwargs['ax'] = None  # plot new fig
            elif 'agg' in kwargs['mode']:
                kwargs['ax'] = None
                kwargs['title'], legend_keys = self.get_title(grouped_analyses)
                filename, _ = self.get_title(grouped_analyses, shorten = True)
                kwargs['show_legend'] = False
            else:
                if grouped_analysis == None:
                    raise Exception('Dummy plot is not allowed')
                kwargs['ax'] = None
                kwargs['title'] = self.get_title2(grouped_analysis)
                filename = self.get_title2(grouped_analysis, True)

            # overwrite auto-generated legend label if custom labels are provided
            if kwargs.get('overwrite_legends', None):
                if count < len(kwargs['overwrite_legends']):
                    kwargs['original_label'] = kwargs['label']
                    kwargs['label'] = kwargs['overwrite_legends'][count]
            if 'overlay' in kwargs['mode']:
                kwargs['max_x'] = None
                kwargs['label'] = [logfolder[0][-4:] for logfolder in grouped_analysis.get_label('logfolder')]  # list of list of a single element which is the path of logfolder, extract last 4 chars
                if isinstance(kwargs['label'], list) and len(stacked_y) > len(kwargs['label']):
                    if all([kwargs['label'][0] == v for v in kwargs['label']]):
                        kwargs['label'] = kwargs['label'][0]
                    else:
                        kwargs['label'] = list2string(lsof_strings=kwargs['label'], sort=False, linebreak=False, delimiter='_')
                kwargs = plot_data(episodes, stacked_y, None, **kwargs)
                # TODO: should this be removed?
                # if kwargs['save_legend_in_fig']:
                #     kwargs['save_legend_in_fig'] = False
                #     kwargs['show_legend'] = True
            else:
                kwargs = plot_data(episodes, agg_y, std_dev, **kwargs)

#            # sort legend
#            if 'cross' not in kwargs['mode'] or count == len(grouped_analyses):
#                handles, labels = kwargs['ax'].get_legend_handles_labels()
#                # sort both labels and handles by labels
#                labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
#                kwargs['ax'].legend(handles, labels)

            count += 1
            if (save_fig and 'cross' not in kwargs['mode']) or ('cross' in kwargs['mode'] and count == len(order)):       # use len(order) instead of len(grouped_analyses) because some analysis might be skipped
                filename = filename.replace('\n','_').replace(' ','_').replace(':', '-') + "_" + \
                            list2string(lsof_strings=kwargs['mode'], sort=False, linebreak=False, delimiter='__') + \
                            "." + kwargs['format']
                folder = self.logfolder
                if not os.path.isdir(folder):
                    os.makedirs(folder)
                kwargs['fig'].set_size_inches(kwargs['figsize'][0], kwargs['figsize'][1])
                
                if 'cross' in kwargs['mode']:
                    if fig_num == None:
                        fig_num = gen_num(folder, filename[: filename.rfind('.')])      # do not generate a new fig_num as we want to overwrite the figure if using 'cross'
                else:
                    fig_num = gen_num(folder, filename[: filename.rfind('.')])
                
                filename = filename[: filename.rfind('.')] + '__' + fig_num + filename[filename.rfind('.') :]
                if kwargs['save_legend_in_fig'] and kwargs.get('ax', None) and kwargs['ax'].get_legend():
                    save_legend_as_figure(kwargs['ax'].get_legend(), os.path.join(folder, filename[: filename.rfind('.')]+'__legend.png'))
                    kwargs['ax'].get_legend().remove()
                # if use bbox_inches, this will prevent figure from cropping off stuff, however, title wrap no longer works
                plt.savefig(os.path.join(folder, filename), format=kwargs['format'], bbox_inches="tight", dpi=kwargs['dpi'])
                plt.close(plt.gcf())                                                    # save memory by closing current figure
            if 'original_label' in kwargs and isinstance(kwargs['original_label'], str) and kwargs['original_label']:
                legend_labels += '\n' + kwargs['original_label']                        # write original legend label to text file instead of custom label
            elif isinstance(kwargs['label'], str) and kwargs['label']:
                legend_labels += '\n' + kwargs['label']
            if show_fig:
                kwargs['fig'].show()
        if legend_labels and folder != '':            # if folder == '', means nothing is plotted (this happens if a metric is not avaiable such as num of features for PROST)
            if save_fig:
                f = open(os.path.join(folder, 'legend.txt'), "a")
                f.write(legend_labels+'\n')
                f.close()
            else:
                print(legend_labels)
        plt.close()

    def plot_time_taken(self, grouped_analyses):
        for analysis in grouped_analyses:
            analysis.print_time_taken()

    def get_grouped_data(self, analyses, **kwargs):
        cache = []               # list of dicts from analysis.get_attributes() that have been extracted thus far
        grouped_data = []        # each element is the aggreagted results over a set of experiments
        grouped_analyses = []    # each element is a list of analyses that are have the same settings
        kwargs_copy = copy.deepcopy(kwargs)

        # loop through and find analysis that has not been added to cache
        for analysis in analyses:
            kwargs_copy.update(analysis.get_attributes())
            # check if analysis is in cache
            if not dict_in_list_of_dict(cache, kwargs_copy, kwargs_copy['identifier']):
                # records analaysis that has been grouped already, each analysis can only be in 1 group
                cache.append(analysis.get_attributes())
                # extract analyses that have same identifier
                analyses_to_compare = get_common_data(analyses, **kwargs_copy)
                if len(analyses_to_compare) == 0:
                    string = "Number of analyses for identifiers" 
                    for key in kwargs_copy['identifier']:
                        if key in kwargs_copy:
                            string += " " + str(key) + ": " + str(kwargs_copy[key])
                    string += " is zero"
                    raise Exception(string)
                grouped_analyses.append(analyses_to_compare)

                if 'mode' in kwargs_copy:
                    # extract data from each analysis
                    dataType = get_data_type(kwargs_copy.get('mode', []))
                    # if dataType == 'computation_time_per_round':
                    #     computation_hardware = [analysis.get_attribute('computation_hardware') for analysis in self.analyses_to_compare]
                    #     if computation_hardware.count(computation_hardware[0]) != len(computation_hardware):                    # this returns True if at least one element in computation_hardware is different from the other elements
                    #         print('Computation time cannot be compared when hardware is different', end = '')
                    #         print(computation_hardware)
                    #         return None
                    # 3D matrix: (run #, episode #, step #)
                    results = [analysis.get_data(dataType) for analysis in analyses_to_compare]
                    if dataType == 'time_taken':
                        stacked_y = results
                    else:
                        # resizing will not work as it affects computation of std dev and mean
                        # as extra entries are filled with zeros
#                        max_shape = max([y.shape for y, sd in results])
#                        stacked_y = []
#                        for y, sd in results:
#                            yy = y.copy()
#                            yy.resize(max_shape, refcheck = False)
#                            stacked_y.append(yy)
                        try:
                            stacked_y = np.stack( [y for y, _ in results] )
                        except:
                            matrixSizes = [len(result[0]) for result in results]
                            logfolders = [analysis.get_attribute('logfolder') for analysis in analyses_to_compare]
                            string = 'Size of \"' + dataType + '\" does not match...'
                            for matrixSize, logfolder in zip(matrixSizes, logfolders):
                                string += '\n     Logfolder: ' + list2string(logfolder) + ' has size ' + str(matrixSize)
                            raise Exception(string)
                            # correct_size = random.choice(results)[0].size
                            # wrong_instances = ''
                            # count = 0
                            # for y, sd in results:
                            #     count = count+1
                            #     if correct_size != y.size:
                            #         wrong_instances = wrong_instances + str(count) + ' '
                            # raise Exception("Size of \"" + dataType + 
                            #                 "\" does not match for analyses of " +
                            #                 "Instance: " + kwargs_copy['instance'] + 
                            #                 ", Planner: " + kwargs_copy['planner'] +
                            #                 ", Policy: " + kwargs_copy['policy'] +
                            #                 ", #: " + wrong_instances)
                    
                    # if using random instance per episode or repetition, then overwrite instances to _RPE or _RPR to indicate so
                    attributes = [analysis.get_attribute('instance') for analysis in analyses_to_compare]
                    if all([is_rpg_instance(attribute) for attribute in attributes[0]]):
                        instance = parse_instance(attributes[0])
                        if not all(attr == attributes[0] for attr in attributes):
                          if isinstance(attributes[0], list) and len(attributes[0]) > 1:
                              kwargs_copy['instance'] = instance[0]+'__'+instance[1]+'_'+RPG_SUFFIX['per_episode']
                          elif isinstance(attributes[0], list) and len(attributes) > 1:
                              kwargs_copy['instance'] = instance[0]+'__'+instance[1]+'_'+RPG_SUFFIX['per_repetition']
                    # this is for labelling legends in plots of overlaying individual runs (mode = 'overlay')
                    identifier = get_identifier(**kwargs_copy)
                    identifier['logfolder'] = [analysis.get_attribute('logfolder') for analysis in analyses_to_compare]
                    episodes = [analysis.episodes for analysis in analyses_to_compare]
                    if not all([v == episodes[0] for v in episodes]):
                        print(episodes)
                        raise Exception('episodes must be the same for all analyses in analyses_to_compare, check that get_common_data is defined correctly')
                    else:
                        episodes = episodes[0]
                    grouped_data.append( absT.DataMatrices(dataType, stacked_y, identifier, analysis.get_num_steps_per_episode(), analysis.get_num_episodes_per_step(), episodes) )
                    del stacked_y
                    del results
                    gc.collect()
        if 'mode' in kwargs_copy:
            del cache
            del grouped_analyses
            gc.collect()
            return grouped_data
        else:
            del cache
            del grouped_data
            gc.collect()
            return grouped_analyses
        # this portion of the code is never tested, not needed as MultiAnalysis
        # consist of analyses from the same instance
        # sort grouped_data by instances
#        sorted_grouped_data = []
#        while len(grouped_data) > 0:
#            insert_this_data = grouped_data.pop(0)
#            sorted_grouped_data.append(insert_this_data)
#            index = 0
#            del_list = []   # list of index that have been inserted to sorted_grouped_data
#            for data in grouped_data:  # find others that have same instance
#                if insert_this_data.get_attribute('instance') == data.get_attribute('instance'):
#                    sorted_grouped_data.append(data)
#                    del_list.append(index)
#                index += 1
#            del_list.reverse()   # delete from the back else index will change
#            for index in del_list:
#                del grouped_data[index]
#        return sorted_grouped_data

    # find attributes that are common in all analyses, then use it as the figure title
    # analyses is of Class DataMatrices
    def get_title(self, analyses, exclude_legend_keys = None, shorten = False):
        verbose = 0
        keys_w_different_attributes = []
        keys_w_common_attributes = []
        title = []
        using_rpg = False
        use_domain_in_title = True
        use_learner = analyses[0].get_attribute('learner') != None and analyses[0].get_attribute('learner') != 'None'
        use_mps = any(\
            [analysis.get_numeric_attribute('beam_search_branch') > 1 or \
             analysis.get_numeric_attribute('num_hypothesis_domains') > 1 or \
             analysis.get_numeric_attribute('rollout_horizon') > 0 or \
             len(analysis.get_attribute('planners')) > 1
             for analysis in analyses])
        for key in title_keys:
            if shorten and key not in shorten_title_keys:
                continue
            if key == 'domain' or (not use_learner and (key == 'max_round_for_ml' or key == 'beam_search_branch')):
                continue
            # if not use_learner and (key == "learner" or key == "beam_search_branch"):
            #     continue
            if not use_mps and (key == 'num_hypothesis_domains' or key == 'rollout_horizon' or key == 'multi_planning'):
                continue
            same_attributes = True
            attribute = analyses[0].get_attribute(key)                          # this line is needed if all attributes are None
            # find any attribute that it != None or '' and use it for subsequent comparisons
            attributes = [analysis.get_attribute(key) for analysis in analyses]
            for attribute_ in attributes:
                if attribute_ != None and attribute_ != '':
                    attribute = attribute_
                    break
            if attribute == None:                                               # instance attribute will be None if running multi-instances per session
                if verbose > 1:
                    print("Can't find attribute " + key + " - omit from title")
                continue
            # now check for all other analyses if the attribute matches analyses[0]
            for analysis in analyses:
                if analysis.get_attribute(key) != attribute:
                    same_attributes = False
                    if exclude_legend_keys == None or key not in exclude_legend_keys:
                        keys_w_different_attributes.append(key)
                        if verbose > 0:
                            print('Different attributes for '+key)
                    break
            if same_attributes:
                keys_w_common_attributes.append((key, attribute))
                if verbose > 1:
                    print('Common attributes for '+key)
                if key == 'instance':
                    using_rpg = all([is_rpg_instance(attri) for attri in attributes])   # using random instance per repetition
        
        merge_string_for_FA = ''
        merge_string_for_FL = ''
        merge_string_for_IR = ''

        for key, attribute in keys_w_common_attributes:
            if key == 'instance':
                if using_rpg:
                    title.append(attribute)
                else:
                    title.append(get_attribute_label(key, attribute))
                use_domain_in_title = False
            elif key != 'logfolderID':
                if 'function_approximation' in key:                             # this puts all attributes for function_approximation within {}
                    string = get_attribute_label(key, attribute)
                    if ':' in string:
                        string = string[string.find(':')+1 :].strip()           # remove prefix text
                    if merge_string_for_FA == '':
                        merge_string_for_FA = '{FA: ' + string                  # add back prefix text only once
                    else:
                        merge_string_for_FA += ' ' + string
                elif 'features_learner' in key:
                    string = get_attribute_label(key, attribute)
                    if ':' in string:
                        string = string[string.find(':')+1 :].strip()
                    if merge_string_for_FL == '':
                        merge_string_for_FL = '{FL: ' + string
                    else:
                        merge_string_for_FL += ' ' + string
                elif 'intrinsic_reward' in key:
                    string = get_attribute_label(key, attribute)
                    if ':' in string:
                        string = string[string.find(':')+1 :].strip()
                    if merge_string_for_IR == '':
                        merge_string_for_IR = '{IR: ' + string
                    else:
                        merge_string_for_IR += ' ' + string
                else:
                    if merge_string_for_FA:                                     # if key has changed, add string to title
                        title.append(merge_string_for_FA + '}')
                        merge_string_for_FA = ''                                # clear string to avoid adding again
                    elif merge_string_for_FL:
                        title.append(merge_string_for_FL + '}')
                        merge_string_for_FL = ''
                    elif merge_string_for_IR:
                        if merge_string_for_IR.strip() != '{IR:':
                            title.append(merge_string_for_IR + '}')
                            merge_string_for_IR = ''
                    title.append(get_attribute_label(key, attribute))
        if use_domain_in_title:
            attribute = get_attribute_label('domain', analyses[0].get_attribute('domain'))
            title.insert(0, attribute)
        return (list2string(lsof_strings=title, sort=False, linebreak=True, delimiter=' '), keys_w_different_attributes)

    # find attributes that are common in all analyses, then use it as the title
    def get_title2(self, analysis, shorten = False):
        title = []
        use_domain_in_title = True
        use_learner = analysis.get_attribute('learner') != None and analysis.get_attribute('learner') != 'None'
        use_mps = \
                  analysis.get_numeric_attribute('beam_search_branch') > 0 and \
                  analysis.get_numeric_attribute('num_hypothesis_domains') > 0 and \
                  analysis.get_numeric_attribute('rollout_horizon') > 0
        for key in title_keys:
            if shorten and key not in shorten_title_keys:
                continue
            if key == 'domain' or key == 'logfolderID':
                continue
            if key == 'instance':        # if RPG experiments, print instances
                if analysis.get_attribute('is_multi_tasks') and \
                    (RPG_SUFFIX['per_repetition'] not in get_attribute_label(key, analysis.get_attribute(key)) and \
                    RPG_SUFFIX['per_episode'] not in get_attribute_label(key, analysis.get_attribute(key))) :
                    continue
                else:
                    use_domain_in_title = False
            if not use_learner and (key == "learner" or key == "beam_search_branch"):
                continue
            if not use_mps and (key == "num_hypothesis_domains" or key == "rollout_horizon" or key == "multi_planning"):
                continue
            attribute = get_attribute_label(key, analysis.get_attribute(key))
            if attribute:
                title.append(attribute)
        if use_domain_in_title:
            attribute = get_attribute_label('domain', analysis.get_attribute('domain'))
            title.insert(0, attribute)
        return list2string(lsof_strings=title, sort=False, linebreak=True, delimiter=' ') 

# data is a list of Class Analysis or Class absT.DataMatrices
def set_logfolderID(lsof_data, truncate_last_few_folders = 2):
    # perform correction for logfolderID
    # Example: 2 folders with folderA/subfolderB and folderC/subfolderB will have the same logfolderID despite having different paths
    # Then, logfolderID should include folderA_subfolderB, folderC_subfolderB
    logfolders = [data.get_attribute('logfolder') for data in lsof_data]
    if None not in logfolders:                                      # if at least one data has no logfolder defined, then we can't find longest common sub-path of logfolder
        longest_common_index = 1000
        prev_logfolder = []
        for logfolder in logfolders:
            logfolder = os.path.normpath(logfolder[0]).split(os.sep)  # split logfolder into list of strings
            if not prev_logfolder:                                  # true for 1st iteration
                prev_logfolder = logfolder
                continue
            index = 0
            for prev, current in zip(prev_logfolder, logfolder):    # iterate from root folder to subfolders
                if prev != current:
                    break                                           # mismatch in subfolder
                else:
                    index += 1                                      # matches, increase index count
                    if index >= longest_common_index:               # no point to continue, we want to find the smallest index for matching subfolders
                        break
            if index < longest_common_index:
                longest_common_index = index
        for i in range(len(lsof_data)):
            logfolder = os.path.normpath(logfolders[i][0]).split(os.sep)
            folder = logfolder[longest_common_index:-truncate_last_few_folders]  # do not consider last folder which is experiment_<domain>_<planner>_<policy>_000# and 2nd last folder which is <domain>
            if folder:                                              # if logfolders are exactly the same, then folder = []
                lsof_data[i].delete_attribute('logfolderID')        # delete key from dict before set_attribute, else it will append to existing value rather than overwrite
                lsof_data[i].set_attribute('logfolderID', list2string(lsof_strings=folder, sort = False, linebreak = False, delimiter='_'))

def get_attribute_label(key, attribute):
    if attribute == None:
        # print("Can't find attribute " + key + " - omit from title")
        return ''
    elif isinstance(attribute, bool) and not attribute:
        return ''
    else:
        if not isinstance(attribute, str):
            attribute = str(attribute)
        if attribute == '' or attribute.lower() == 'none' or attribute.lower() == 'disabled':
            return ''
    if key == 'initial_domain' and attribute:
        attribute = 'Prior:' + attribute
    if key == 'latent_objects' and attribute:
        attribute = 'Latent-Obj:' + attribute
    if key == 'dynamic_constraints' and attribute:
        attribute = 'Dyn-C:' + attribute
    if key == 'model_representation' and attribute:
        attribute = 'MDL:' + attribute
    if key == 'experience' and attribute:
        attribute = 'EXP:' + attribute
    if key == 'function_approximation' and attribute:
        attribute = 'FA:' + attribute
    if key == 'function_approximation_feature_selection' and attribute:
        attribute = 'FA: ' + attribute
    if key == 'function_approximation_feature_selection_mod' and attribute:
        attribute = 'FA: ' + attribute
    if key == 'function_approximation_context' and attribute:
        attribute = attribute
    if key == 'function_approximation_max_criteria' and attribute:
        attribute = attribute
    if key == 'features_learner' and attribute:
        attribute = 'FL:' + attribute
    if key == 'features_learner_sync_learning' and attribute:
        attribute = attribute
    if key == 'features_learner_zeta' and attribute:
        attribute = 'zeta=' + attribute
    if key == 'features_learner_initial_feature_size' and attribute:
        attribute = 'I=' + attribute
    if key == 'features_learner_max_feature_size' and attribute:
        attribute = 'M=' + attribute
    if key == 'features_learner_tau' and attribute:
        attribute = 'tau=' + attribute
    if key == 'eligibility_trace_type' and attribute:
        attribute = 'El:' + attribute
    if key == 'loop_detection' and attribute:
        attribute = 'LD:' + attribute
    if key == 'replay_trajectory_to_goal' and attribute:
        attribute = 'Goal-Replay:' + attribute
    if key == 'revert_to_best_policy' and attribute:
        attribute = 'Revert-Policy:' + attribute
    if key == 'beam_search_branch' and attribute:
        attribute = 'Beam:' + attribute
    if key == 'multi_planning' and attribute:
        attribute = 'MPS:' + attribute
    if key == 'num_hypothesis_domains' and attribute:
        attribute = 'HM:' + attribute
    if key == 'rollout_horizon' and attribute:
        attribute = 'RH:' + attribute
    if key == 'max_round_for_ml' and attribute:
        attribute = 'Cutoff:' + attribute
    if key == 'local_min_detection' and attribute:
        attribute = 'LMD:' + attribute
    if key == 'intrinsic_reward' and attribute:
        attribute = 'IR:' + attribute
    if key == 'intrinsic_reward_rmax' and attribute:
        attribute = 'IR-Rmax=' + attribute
    if key == 'intrinsic_reward_beta' and attribute:
        attribute = 'beta=' + attribute
    if key == 'intrinsic_reward_beta_decay' and attribute:
        attribute = 'beta-decay=' + attribute
    # if key == 'intrinsic_reward_experience' and attribute:
    #     attribute = 'IR-Exp=' + attribute
    if key == 'intrinsic_reward_aggregation' and attribute:
        attribute = 'Agg=' + attribute
    if key == 'self_play' and attribute:
        attribute = 'SP:' + attribute
    if key == 'mve_horizon' and attribute:
        attribute = 'MVE:' + attribute
    if key == 'mqte_horizon' and attribute:
        attribute = 'MQTE:' + attribute
    # if key == 'learn_from_failure' and attribute:
        # attribute = 'LfF'
    if key == 'discount_factor' and attribute:
        attribute = 'DF:' + attribute
    if key == 'alpha' and attribute:
        return ''
    if key == 'batch' and attribute:
        return ''
    if key == 'decay' and attribute:
        return ''
    if key == 'epsilon' and attribute:
        return ''
    if key == 'import_intrinsic_reward' and attribute:
        return ''
    if key == 'import_qvalue' and attribute:
        return ''
    if key == 'lambda' and attribute:
        return ''
    if key == 'horizon' and attribute:
        return ''
    return attribute

def get_data_type(mode):
    # if 'norm_rewards' in mode:
    #     return 'norm_rewards'
    if 'original_rewards' in mode:
        return 'original_rewards'
    elif 'rewards' in mode:
        return 'rewards'
    elif 'original_rewards_per_round' in mode:
        return 'original_rewards_per_round'
    elif 'rewards_per_round' in mode:
        return 'rewards_per_round'
    # elif 'rewards_computation_time_per_round' in mode:
    #     return 'rewards_computation_time_per_round'
    elif 'succ_exec' in mode:
        return 'succ_exec'
    elif 'execution_timestamp' in mode:
        return 'execution_timestamp'
    elif 'computation_time_per_round' in mode:
        return 'computation_time_per_round'
    elif 'time_taken' in mode:
        return 'time_taken'
    elif 'num_features_per_round' in mode:
        return 'num_features_per_round'
    elif 'terminal_state' in mode:
        return 'terminal_state'
    elif 'goal_state' in mode:
        return 'goal_state'
    elif 'deadend_state' in mode:
        return 'deadend_state'
    elif 'non_goal_state' in mode:
        return 'non_goal_state'
    else:
        raise Exception("Unrecognised data type '" + list2string(mode) + "' for mode specified")


def get_ylabel(mode):
    if 'norm_rewards' in mode:
        return 'Normalized Rewards'
    elif 'original_rewards' in mode:
        return 'Original Rewards'
    elif 'rewards' in mode:
        return 'Rewards'
    elif 'original_rewards_per_round' in mode:
        return 'Original Rewards'
    elif 'rewards_per_round' in mode:
        return 'Rewards'
    # elif 'rewards_computation_time_per_round' in mode:
    #     return 'Rewards / Computation Time'
    elif 'succ_exec' in mode:
        return 'Successful Execution'
    elif 'execution_timestamp' in mode:
        return 'Elapsed Time (s)'
    elif 'computation_time_per_round' in mode:
        return 'Computation Time (s)'
    elif 'time_taken' in mode:
        return 'Computation Time (s)'
    elif 'num_features_per_round' in mode:
        return 'Num. of Features'
    elif 'terminal_state' in mode:
        # return 'Goal / Deadend States Reached'
        return 'Goal States - Dead Ends'
    elif 'goal_state' in mode:
        return 'Goal States Reached'
    elif 'deadend_state' in mode:
        return 'Dead Ends Reached'
    elif 'non_goal_state' in mode:
        return 'Goal States Not Reached'
    else:
        raise Exception("Unrecognised data type for mode specified: " + mode)


# if linebreak true, insert \n after 1st element of lsof_strings
def list2string(lsof_strings, sort = True, linebreak = False, delimiter = ' '):
    MAX_CHAR_LEN = 1000
    char_len = 0
    if isinstance(lsof_strings, list):
        lsof_strings = [v for v in lsof_strings if isinstance(v, str)]
    elif isinstance(lsof_strings, str):
        lsof_strings = [lsof_strings]
    if lsof_strings == None or lsof_strings == "":
        return ""
    elif len(lsof_strings) == 1:
        return lsof_strings[0]
    elif isinstance(lsof_strings, str):
        return lsof_strings
    s = ""
    if sort:
        lsof_strings.sort()      # sort by alphabetical order
    for value in lsof_strings:
        if isinstance(value, list):
            value = value[0]
        if isinstance(value, str) and value != '':
            s += value
            if linebreak and char_len == 0:
                s += "\n"
            else:
                s += delimiter
            char_len += len(value)
            if char_len >= MAX_CHAR_LEN:
                char_len = 0
    return s[:-len(delimiter)]


def dict2string(dictionary, sort = True):
    values = [(key, value) for key, value in dictionary.items() if isinstance(value, str)]
    if sort:
        values.sort(key = lambda value : value[0])
    return list2string(lsof_strings=[v[1] for v in values], sort=False, linebreak=False, delimiter='_')


def dict_in_list_of_dict(lsof_dict, dict_, keys):
    for d in lsof_dict:
        if same_dict(d, dict_, keys):
            return True
    return False


def same_dict(dict1, dict2, keys):
    for key in keys:
        if key == 'instance':
            if not same_instance(dict1.get(key, None), dict2.get(key, None)):
                return False
        elif dict1.get(key, None) != dict2.get(key, None):
            return False
    return True


def is_rpg_instance(inst):
    return len(parse_instance(inst)) == 3


# Example of a random instance: turtlebot_survey_inst_mdp__1_23
def parse_instance(inst):
    if isinstance(inst, list):
        if len(inst) == 1:
            return parse_instance(inst[0])
        else:
            instances = [parse_instance(inst_) for inst_ in inst]
            if len(instances[0]) == 3:           # is RPG instances
                domain0 = instances[0][0]
                base_instance0 = instances[0][1]
                rpg_instances = [instance[2] for instance in instances]
                for domain, base_instance, rpg_instance in instances:
                    if domain0 != domain:
                        raise Exception('Domain does not match: ' + domain0 + ' vs. ' + domain)
                    # do not check the condition below. if running randomized instances of different base instance
                    # (e.g generalizing from inst1 to inst2) then this condition will be true and exception will be thrown incorrectly
                    # if base_instance0 != base_instance:
                    #     raise Exception('Base instance does not match: ' + base_instance0 + ' vs. ' + base_instance)
                return (domain0, base_instance0, rpg_instances)
            else:
                return instances[0]
    inst_ = (inst[:inst.find('__')], inst[inst.find('__')+2:])
    pos = inst_[1].find('_')
    if pos != -1:
        # is random instance, returns ('turtlebot_survey_inst_mdp', '1', '23')
        return (inst_[0], inst_[1][:pos], inst_[1][pos+1:])
    else:
        return inst_        # not random instance, returns ('turtlebot_survey_inst_mdp', '1')


# checks if same instance by considering 2 random instances of the same base instance as the same
def same_instance(inst1, inst2):
    if isinstance(inst1, list) and isinstance(inst2, list):
        if len(inst1) == len(inst2):
            for inst1_, inst2_ in zip(inst1, inst2):
                if not same_instance(inst1_, inst2_):
                    return False
            return True
        else:
            return False
    if inst1 == None and inst2 != None:
        return False
    elif inst1 != None and inst2 == None:
        return False
    else:
        instance1 = parse_instance(inst1)
        instance2 = parse_instance(inst2)
        if len(instance1) == len(instance2) and instance1[0] == instance2[0] and instance1[1] == instance2[1]:
            return True
        else:
            return False                      # regardless of random instance or not, both are different


def get_identifier(**kwargs):
    identifier = {}
    for key in grouping_keys:
        if key in kwargs:
            if key == 'domain':
              pass
            if isinstance(kwargs[key], list):
                # if running multi-sessions, then attributes (especially instance)
                # might be different, set to None if different
                if key == 'instance':
                    instances = [value for value in kwargs[key]]                # TODO: 
                    using_rpg = all([is_rpg_instance(instance) for instance in instances])
                    if using_rpg:
                        instance = parse_instance(instances[0])
                        if not all(inst == instances[0] for inst in instances):
                            if isinstance(instances[0], list) and len(instances[0]) > 1:
                                identifier[key] = instance[0]+'__'+instance[1]+'_'+RPG_SUFFIX['per_episode']
                            elif isinstance(instances, list) and len(instances) > 1:
                                identifier[key] = instance[0]+'__'+instance[1]+'_'+RPG_SUFFIX['per_repetition']
                        else:
                            identifier[key] = instance[0]
                    else:
                        identifier[key] = None
                elif all(value == kwargs[key][0] for value in kwargs[key]):
                    identifier[key] = kwargs[key][0]
                else:
                    identifier[key] = None
            else:
                identifier[key] = kwargs[key]
    return identifier


def gen_num(path, name = None):
    # get unique filename or folder name
    if name:
        ps = os.popen('ls ' + path + ' | grep ' + name)
        folders = ps.readlines()
        num = 0
        for f in folders:
            f = f.strip()
            if '.' in f:
              f = f[: f.rfind('.')]     # remove file extension
            try:
                num = max([int(f[-4:]), num])
            except:
                pass
    else:
        ps = os.popen('ls ' + path)
        folders = ps.readlines()
        num = 0
        for f in folders:
            try:
                num = max([int(f), num])
            except:
                pass
    return "%04d" % (num+1)


def moving_average(data, n = 3):
    if n <= 1:
        return data
    ret = np.cumsum(data, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    # we do a recursive call on moving_average for data[: n - 1] with a smaller window, else there will be huge spikes at the start followed by smooth plot if n is large
    return np.concatenate((moving_average(data[: n - 1], int(n/4)), ret[n - 1:] / n), axis = 0)
    # return np.concatenate((data[: n - 1], ret[n - 1:] / n), axis = 0)


def generate_all_legend_styles(filename, num = 20):
    fig, ax = plt.subplots()
    for i in range(num):
        ax.plot(0, 0, label='#'+str(i))
    plt.legend(ncol=1, framealpha=1.0, facecolor="white")
    save_legend_as_figure(ax.get_legend(), filename)
    # plt.show()
    # plt.savefig(filename, bbox_inches="tight")
    # plt.close()


def plot_data(x, y, std_dev, **kwargs):
    plot_settings = copy.deepcopy(def_plot_settings)
    plot_settings.update(kwargs)
    moving_avg_window = plot_settings.get('moving_avg_window', 0)
    if moving_avg_window > 0:
        if 'Rewards' in get_ylabel(plot_settings['mode']):
            pass
        elif 'Elapsed Time' in get_ylabel(plot_settings['mode']):
            pass
        else:
            moving_avg_window = 0         # do not smoothen other metrics
    title = list2string(lsof_strings=plot_settings['title'], sort=False, linebreak=True, delimiter=' ')
    if plot_settings.get('ax', None) == None:
        fig, ax = plt.subplots()
        if "stepwise" in plot_settings['mode']:
            xlabel_ = 'Step'
        elif "episodewise" in plot_settings['mode']:
            xlabel_ = 'Episode'
        else:
            xlabel_ = 'Episode'
            
        if "cumsum" in plot_settings['mode']:
            xlabel_ = "Episode"
            # ylabel_ = 'Cumulative ' + get_ylabel(plot_settings['mode'])
            ylabel_ = get_ylabel(plot_settings['mode'])
        elif "terminal" in plot_settings['mode']:
            xlabel_ = "Episode"
            # ylabel_ = 'Total ' + get_ylabel(plot_settings['mode'])
            ylabel_ = get_ylabel(plot_settings['mode'])
        elif "avg" in plot_settings['mode']:
            ylabel_ = 'Average ' + get_ylabel(plot_settings['mode'])
        else:
            ylabel_ = get_ylabel(plot_settings['mode'])
        # if "agg" in plot_settings['mode'] or "cross" in plot_settings['mode']:
        #     ylabel_ = 'Aggregate ' + ylabel_
        # if moving_avg_window > 0:
            # ylabel_ += ' (MWA =' + str(moving_avg_window) + ')'
        ax.set(xlabel = xlabel_, ylabel = ylabel_)
        if plot_settings.get('show_title', None):
            ax.set_title(title, wrap=True)
            
        if plot_settings['show_legend_outside'] and plot_settings['label']:     # only show legend if there is something in it, else python gives warning
            fig.set_size_inches(plot_settings['figsize'][0]*2, plot_settings['figsize'][1])
        else:
            fig.set_size_inches(plot_settings['figsize'][0], plot_settings['figsize'][1])
        kwargs['fig'] = fig
        kwargs['ax'] = ax

    ndims = len(np.shape(y))
    single_point = np.size(y) == 1   # y is a single value, not an array
    if np.size(y) == 0:
        string = kwargs['title'] + ' has no such data of label --> ' + kwargs['ax'].get_ylabel()
        string = string.replace('\n', '   ')
        return kwargs
    
    # quick hack to make plots for rewards have linewidth of 1 only
    if plot_settings['figsize'] == (3, 2) and ('Rewards' in get_ylabel(plot_settings['mode']) or 'Elapsed Time' in get_ylabel(plot_settings['mode'])):
        # linewidth = 1
        linewidth = plot_settings['linewidth']
    else:
        linewidth = plot_settings['linewidth']

    max_y = 0
    
    if ndims == 0:                                  # dummy plot
        kwargs['ax'].plot(0, y, linewidth=linewidth, label=plot_settings['label'])
    elif ndims == 1:
        if single_point:
            x = 1
        elif not x:
            x = range(1, np.shape(y)[0]+1)
        if single_point:
            marker_ = "o"
        else:
            marker_ = plot_settings['marker']

        y = moving_average(y, moving_avg_window)
        max_y = max(abs(y))
        
        if std_dev is None:
            kwargs['ax'].plot(x, y, linewidth=linewidth, label=plot_settings['label'], marker = marker_)
        else:
            if single_point:
                kwargs['ax'].errorbar(x, y, std_dev, label=plot_settings['label'], marker = marker_)
            else:
                line, = kwargs['ax'].plot(x, y, linewidth=linewidth, label=plot_settings['label'], marker = marker_)
                std_dev = moving_average(std_dev, moving_avg_window)
                if plot_settings['y_log_scale']:                        # if sd < yy, then yy - sd is negative which goes to inf in log-scale
                    tol = 1e-9
                    std_dev = [tol if y_ < std_dev_ else std_dev_ for y_, std_dev_ in zip(y,std_dev)]
                face_alpha_value = 0.2
                # edge_alpha_value = 0.3
                shading_color = line.get_color()      # this gets the color of the last plotted line
                # face_shading_color = shading_color[:-1] + (face_alpha_value, )               # last element is the value of alpha, first 3 elements are RGB
                # edge_shading_color = shading_color[:-1] + (edge_alpha_value, )               # last element is the value of alpha, first 3 elements are RGB
                kwargs['ax'].fill_between(x, y-std_dev, y+std_dev, facecolor=shading_color, alpha=face_alpha_value)
                # kwargs['ax'].fill_between(x, y-std_dev, y+std_dev, facecolor=face_shading_color, edgecolor=edge_shading_color)
                # print this to get the numerical value of the last element
                # if y[-1] and std_dev[-1]:
                #     print(get_ylabel(plot_settings['mode']) + ' = ' + str(y[-1]) + ' +/- ' + str(std_dev[-1]))

        # get avg over all steps or episodes for comparison with IPPC results
        title_with_labels = title 
        
        if plot_settings['label']:
            title_with_labels += ' ' + plot_settings['label'] 
        if kwargs['ax'].get_ylabel():
            title_with_labels += ' ' + kwargs['ax'].get_ylabel()
        header, msg = process_IPPC_domains(title_with_labels, y)
        if msg:
            if kwargs.get('ippc_log', None):
                os.makedirs(os.path.dirname(kwargs['ippc_log']), exist_ok=True)
                f = open(kwargs['ippc_log'], 'a+')
                if os.path.getsize(kwargs['ippc_log']) == 0:    # file is empty, write header
                  f.write(header+'\n')
                f.write(msg+'\n')
                f.close()
                print('----------------\nWrite IPPC results to ' + kwargs['ippc_log']+'\n----------------')
            else:
                print(msg)

    elif ndims == 2:
        counter = 0
        x = range(1, np.shape(y)[1]+1)
        if (isinstance(std_dev == None, bool) and std_dev == None) or (std_dev == None).any():
            for yy in y:
                # yy = moving_average(yy, moving_avg_window)
                single_point = np.size(yy) == 1   # yy is a single value, not an array
                if single_point:
                    x = 1
                else:
                    x = range(1, np.shape(yy)[0]+1)
                if single_point:
                    marker_ = "o"
                else:
                    marker_ = plot_settings['marker']
                max_y = max(max_y, max(abs(yy)))
                if isinstance(plot_settings['label'], list):
                    kwargs['ax'].plot(x, yy, linewidth=linewidth, label=plot_settings['label'][counter], marker=marker_)
                else:
                    kwargs['ax'].plot(x, yy, linewidth=linewidth, label="Run #"+str(counter+1), marker=marker_)
                counter += 1
        else:            
            for yy, sd in zip(y, std_dev):
                yy = moving_average(yy, moving_avg_window)
                sd = moving_average(sd, moving_avg_window)
                max_y = max(max_y, max(abs(yy)))
                if plot_settings['y_log_scale']:                        # if sd < yy, then yy - sd is negative which goes to inf in log-scale
                    tol = 1e-9
                    sd = [tol if yy_ < sd_ else sd_ for yy_, sd_ in zip(yy,sd)]
                kwargs['ax'].plot(x, yy, linewidth=linewidth, label="Episode "+str(counter+1),marker=plot_settings['marker'])
                kwargs['ax'].fill_between(x, yy-sd, yy+sd, alpha=0.2)
                counter += 1
    else:
        raise Exception("ndims for y cannot exceed 2.")

    
    min_x = 1
    if single_point:
        max_x = 2
    else:
        max_x = int(max(x))
    if kwargs.get('max_x', None):
        if kwargs['max_x'] > max_x:
            max_x = kwargs['max_x']     # need this as not all plots have the same x-limits
        else:
            kwargs['max_x'] = max_x
    else:
        kwargs['max_x'] = max_x
    div = max_x - min_x
    if div % 10 < 5:
        div = int(div / plot_settings['x_num_div'])
    else:
        div = int((div + 10) / plot_settings['x_num_div'])
    if div == 0:
        div = 2
    
    # if max_x >= 1000 and plot_settings['sci']:
    #   kwargs['ax'].ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    if max_y >= 1000 and plot_settings['sci'] and not plot_settings['y_log_scale']:
        kwargs['ax'].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    
    plt.xticks(range(min_x, max_x+div, div))
    plt.xlim(min_x, max_x)
    if plot_settings['y_log_scale']:
        plt.yscale('log')

    if plot_settings.get('y_lim', None):
        ylim = plot_settings['y_lim']
        if len(ylim) > 2:
            plt.yticks(range(ylim[0], ylim[1]+ylim[2], ylim[2]))
        if len(ylim) >= 2:
            plt.ylim(ylim[0], ylim[1])

    if plot_settings['label']:                            # only show legend if there is something in it, else python gives warning
        if plot_settings['show_legend'] or plot_settings['save_legend_in_fig']:
            kwargs['ax'].legend(ncol=plot_settings['legend_ncol'], loc='best', framealpha=1.0)
        elif plot_settings['show_legend_outside']:        # only show legend if there is something in it, else python gives warning
            kwargs['ax'].legend(ncol=plot_settings['legend_ncol'], loc='upper right', framealpha=1.0, bbox_to_anchor=(1.1, 1.1))
            # plt.tight_layout(rect=[0,0,0.75,1])
        handles, labels = kwargs['ax'].get_legend_handles_labels()
        # flip order of legend so that it goes from left to right, up to down RATHER than up to down, left to right
        plt.legend(flip(handles, plot_settings['legend_ncol']), flip(labels, plot_settings['legend_ncol']), ncol=plot_settings['legend_ncol'], loc='best', framealpha=1.0)
        
    if plot_settings['show_grid']:
        plt.grid(color='k', linestyle='-', linewidth=1, alpha=0.2)
    if plot_settings['show_fig']:
        plt.show()
    return kwargs


# flip legend order, instead of going down the columns, it goes across columns
#     1   3
#     2   4
# becomes
#     1   2
#     3   4
def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


# desc is a string which contains information about the experiment setup
# scores is a vector with each row containing the reward accumulated in an episode
def process_IPPC_domains(desc, scores):
    return None, None                                     # DISABLE
    if 'Original Rewards' not in desc:                    # can only compare if scores are original rewards (rewards without RL augmentation)
        return None, None
    instance = desc[: desc.find('\n')]
    prost_scores = PROST_IPPC2014.get(instance, None)
    if prost_scores == None:
        return None, None
    function_approximation = ''
    if 'FA=' in desc:
        function_approximation = desc[desc.find('FA=')+3 :]
    elif 'FA:' in desc:
        function_approximation = desc[desc.find('FA:')+3 :]
    if function_approximation:
        function_approximation = function_approximation[: function_approximation.find(' ')]
        if function_approximation and not function_approximation[-1].isalnum():        # remove trailing commas if any
            function_approximation = function_approximation[:-1]

    features_learner = ''
    if 'FL=' in desc:
        features_learner = desc[desc.find('FL=')+3 :]
    elif 'FL:' in desc:
        features_learner = desc[desc.find('FL:')+3 :]
    if features_learner:
        features_learner = features_learner[: features_learner.find(' ')]
        if features_learner and not features_learner[-1].isalnum():        # remove trailing commas if any
            features_learner = features_learner[:-1]

    # hackish way to get algorithm
    algorithm = ''
    algorithms = ['Q-Learning', 'Double Q-Learning', 'Q(lambda)', 'SARSA', 'SARSA(lambda)']
    for algo in algorithms:
      if algo in desc:
        algorithm = algo
        break

    raw_score = sum(scores)/len(scores)
    # norm_score = (raw_score-prost_scores['min_score']) / (prost_scores['max_score']-prost_scores['min_score'])
    # norm_score = (raw_score-prost_scores['min_score']) / (prost_scores['raw_score']-prost_scores['min_score'])
    norm_score = (raw_score-prost_scores['raw_score']) / abs(prost_scores['raw_score']) 
    # if norm_score < 0:
    #     norm_score = 0
    # elif norm_score > 1:
    #     norm_score = 1

    # msg = instance + '\tFA=' + function_approximation + \
    #       '\tNorm=' + "{:.2f}".format(norm_score) + \
    #       '\tRaw-Avg-Reward=' + "{:.2f}".format(raw_score) + \
    #       '\tRaw-Min-Reward=' + "{:.2f}".format(min(scores)) + \
    #       '\tRaw-Max-Reward=' + "{:.2f}".format(max(scores))
    header = 'Instance'
    msg = instance
    if function_approximation:
      header += '\tFunction Approx'
      msg += '\t' + function_approximation
    if features_learner:
      header += '\tFeature Learner'
      msg += '\t' + features_learner
    if algorithm:
      header += '\tAlgorithm'
      msg += '\t' + algorithm

    header += '\tNorm Score\tRaw Score\tMin Score\tMax Score'
    msg += '\t' + "{:.4f}".format(norm_score) + \
           '\t' + "{:.4f}".format(raw_score) + \
           '\t' + "{:.4f}".format(min(scores)) + \
           '\t' + "{:.4f}".format(max(scores))
    return header, msg