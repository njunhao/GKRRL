    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:10:13 2019

@author: alvin
"""

import sys
import os
import copy   # deep copy
import importlib
import matplotlib.pyplot as plt
import common_utils
import parser
import analysis_type as aysT

if os.getcwd().find('/mbrrl/') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl/')+len('/mbrrl/')]
elif os.getcwd().find('/mbrrl') >= 0:
    mbrrl_path = os.getcwd()[:os.getcwd().find('/mbrrl')+len('/mbrrl')]
else:
    raise("Unable to determine library path, current directory is " + os.getcwd())

DOMAINS = ['tiago_hri', 'taxi', 'grid_survey', 'robot_inspection', 'recon2', 'orca_inspection', 'husky_inspection', 'turtlebot', 'turtlebot_goal', 'turtlebot_survey', 'tiago', 'tiago_fetch', 'triangle_tireworld', 'crossing_traffic', 'elevators', 'game_of_life', 'navigation', 'academic_advising', 'wildfire', 'recon', 'skill_teaching', 'tamarisk', 'sysadmin', 'blocksworld']
settings = {}

############## CHOOSE PROPERTIES OF EXPERIMENTS TO ANALYSE ##############
settings['domains'] = []                        # set to empty to plot all
settings['planners'] = []
settings['policies'] = []

############## CHOOSE LOGFOLDERS TO ANALYSE ##############
settings['logfile'] = 'mbrrl.log'
settings['ace_logfile'] = 'blocks.results'
# settings['logfile'] = 'mbrrl_console.log'     # full logfile, takes longer to parse
settings['quick_plotting'] = 0                  # if > 0, only plot folders with numbering that is a multiple of quick_plotting

# logfiles from all folders will be analysed (useful for analysing across different experiment runs)
# FORMAT: list of strings OR list of 2-element tuple where (string for folder, list of numbers for which subfolder with such number will be analysed)
# Example: ('recon2', [1, 2]) --> then recon2/experiment_recon2_doubleq_epsilon_0001, recon2/experiment_recon2_doubleq_epsilon_0002 will be analysed
settings['folders_to_analyse'] = []

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
# settings['plot_options'].append(['execution_timestamp', 'cross'])
# settings['plot_options'].append(['original_rewards', 'terminal', 'cross'])
settings['plot_options'].append(['rewards', 'terminal', 'cross'])
settings['plot_options'].append(['num_features_per_round', 'cross'])
settings['plot_options'].append(['terminal_state', 'cumsum', 'cross'])

# settings['plot_options'].append(['succ_exec', 'cumsum', 'cross'])
# settings['plot_options'].append(['goal_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['deadend_state', 'cumsum', 'cross'])
# settings['plot_options'].append(['non_goal_state', 'cumsum', 'cross'])

#       CONCATENTATE: concatenate episodes from different logfolders as if they were from one single repetition
#           [logfolder1/0001 logfolder2/0001 logfolder3/0001 ...]
#           [logfolder1/0002 logfolder2/0002 logfolder3/0002 ...]
# settings['plot_options'] = [po+['concatenate'] for po in settings['plot_options']]

#       CONCATENTATE & AGGREGATE: concatenate episodes from different logfolders as if they were from one single repetition, then aggregate them
#           [logfolder1/0001 logfolder2/0001 logfolder3/0001 ...]
#           [logfolder1/0002 logfolder2/0002 logfolder3/0002 ...]
# settings['plot_options'] = [po+['concatenate-agg'] for po in settings['plot_options']]

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
# settings['grouping_keys'].append(['domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection_mod'])

# # compare selfplay horizon
# settings['grouping_keys'].append(['domain', 'initial_domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'intrinsic_reward', 'num_hypothesis_domains'])
# # compare selfplay true vs. learned models
# settings['grouping_keys'].append(['domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'self_play', 'intrinsic_reward', 'num_hypothesis_domains'])
# # compare selfplay num of hypothesis models
# settings['grouping_keys'].append(['domain', 'initial_domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'intrinsic_reward', 'self_play'])
# # compare intrinsic reward
# settings['grouping_keys'].append(['domain', 'initial_domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'num_hypothesis_domains', 'self_play'])

# compare intrinsic reward
# settings['grouping_keys'].append(['domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'intrinsic_reward_beta'])
# settings['grouping_keys'].append(['domain', 'instance', 'function_approximation_max_criteria', 'function_approximation_feature_selection', 'intrinsic_reward'])

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
    'x_num_div': 6,
    'y_lim': None,                  # (y_min, y_max) or (y_min, y_max, y_div)
    'moving_avg_window': 10,        # only applied when plotting rewards or mission time
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
    'fontsize': 10,
    'dpi': 100,
    'format': 'png',
    # line settings
    'color': 'k',
    'linestyle': '-',
    'linewidth': 2,
    'marker': None,
    'alpha': 1,
    # analysis settings
    'mode': [],
    'remove_outlier': [0, 0]    # [num of argmin, num of argmax] to remove, otherwise use a num which is equivalent to [num, num]
}
###################################################

def get_common_folder(folders):
    # generate a common folder for list of folders to save figures in
    paths = []
    for path in [f.split('/') for f in folders if f]:
        paths.append([p for p in path if p != ''])           # remove empty string
    path_is_common = True
    common_path = []
    index_common_path = -1
    while path_is_common:
        index_common_path = index_common_path+1
        if index_common_path >= len(paths[0]):
            break
        elif paths[0][index_common_path]:
            prev_p = paths[0][index_common_path]
        else:
            continue        # skip empty string
        for p in paths:
            if index_common_path >= len(p) or p[index_common_path] != prev_p:
                path_is_common = False
                break
        if path_is_common:
            common_path.append(prev_p)

    # name of the last folder is the merged names of the set of the first dismatching folder names
    merged_name = []
    for p in paths:
        if index_common_path < len(p):
            # this is to get rid of trailing folders in a path such as 'experiment_domain_...'
            max_substring_allowed = 3
            subfolders = p[index_common_path:index_common_path+max_substring_allowed]
            for i in range(len(subfolders)):
                if 'fig_' in subfolders[i] or 'experiment_' in subfolders[i] or '.' in subfolders[i] or any([subfolders[i] == d for d in DOMAINS]):
                    subfolders = subfolders[:i]
                    break
            merged_name.append(aysT.list2string(subfolders, sort=False, linebreak=False, delimiter='-'))  # merged name from the first dismatching folder till the last folder
    merged_name = list(dict.fromkeys(merged_name))      # remove duplicates
    common_path.append(aysT.list2string(lsof_strings=merged_name, sort=False, linebreak=False, delimiter='___'))
    return '/'+os.path.join(*common_path)


# FORMAT for input: list of strings OR list of 2-element tuple where (string for folder, list of numbers for which subfolder with such number will be analysed)
# Example: ('recon2', [1, 2]) --> then recon2/experiment_recon2_doubleq_epsilon_0001, recon2/experiment_recon2_doubleq_epsilon_0002 will be analysed
def merge_folders(folders):
    keyed_folders = {}
    merged_folders = []
    for folder in folders:
        if isinstance(folder, tuple):
            if len(folder) != 2:
                raise Exception('Invalid format for input, must be tuple with 2 elements')
            if isinstance(folder[1], str):
                keyed_folders[folder[0]] = keyed_folders.get(folder[0], []) + [folder[1]]
            elif isinstance(folder[1], list):
                keyed_folders[folder[0]] = keyed_folders.get(folder[0], []) + folder[1]
            else:
                raise Exception('Invalid format for input, 2nd element must be str or list')
        elif isinstance(folder, str):
            merged_folders.append([folder])         # no key to identify this folder, just append it by itself
        else:
            raise Exception('Invalid format for input, must be tuple with 2 elements or a str')
    for key, folders in keyed_folders.items():
        merged_folders.append((key, folders))
    return merged_folders


# def common_start(sa, sb):
#     """ returns the longest common substring from the beginning of sa and sb """
#     def _iter():
#         for a, b in zip(sa, sb):
#             if a == b:
#                 yield a
#             else:
#                 return
#     return ''.join(_iter())


# return True if analysis is to be filtered
def pass_filter(analysis, filter_condition, verbose = False):
    analysis_properties = analysis.get_attributes()
    for key, value in filter_condition.items():
        filters_prop = filter_condition[key]
        a_prop = analysis_properties.get(key, None)
        # a_prop is a list if multiple sessions
        if isinstance(a_prop, list):
            # if running multi-sessions, then attributes (especially instance)
            # might be different, set to None if different
            if all(value == a_prop[0] for value in a_prop):
                a_prop = a_prop[0]
            else:
                a_prop = None   # do not filter on condition if all attributes are not the same

        if filters_prop and a_prop:
            if not isinstance(filters_prop, list):
                filters_prop = [filters_prop]
            filters_prop = [f.lower() for f in filters_prop]
            if a_prop.lower() not in filters_prop:
                if verbose:
                    print('Analysis ' + key + ' = ' + a_prop + ' which does not match filter')
                return False
    return True


def get_logfolders(folders):
    logfolders = []
    unknown_logfolders = []
    for i in range(len(folders)):
        specified_nums = []
        if isinstance(folders[i], tuple) and len(folders[i]) == 2:                   # if is tuple, then is (folder, list of numbers where only subfolders with one of these numbering will be analysed)
            specified_nums = folders[i][1]
            folders[i] = common_utils.remove_prefix(folders[i][0])
        else:
            folders[i] = common_utils.remove_prefix(folders[i])
        if not os.path.isdir(folders[i]):
            continue
        subfolders = os.listdir(folders[i])
        for subfolder in subfolders:
            subfolder = folders[i]+'/'+subfolder
            if os.path.isdir(subfolder):
                logfolders.append(subfolder)
                new_logfolders = [subfolder+'/'+f for f in os.listdir(subfolder)]
                for folder in new_logfolders:
                    if os.path.isdir(folder):
                        try:
                            num = int(folder[folder.rfind('_')+1 :])
                            if specified_nums:
                                if num in specified_nums:
                                    logfolders.append(folder)
                                    # print("Add folder because its number (" + str(num) + ") is in list of specified numbers")
                                # else:
                                #     print("Skip folder because its number (" + str(num) + ") is not in list of specified numbers")
                            else:
                                logfolders.append(folder)       # only add valid logfolder which will have a num in its folder
                        except ValueError:
                            unknown_logfolders.append(folder)
                            continue
        if os.path.isdir(folders[i]):
            logfolders.append(folders[i])
    mbrrl_logfolders = []
    ace_logfolders = []                                                              # for ACE Prolog experiments
    for logfolder in logfolders:
        if os.path.isdir(logfolder):
            if settings['logfile'] in os.listdir(logfolder):
                mbrrl_logfolders.append(logfolder)
            elif settings['ace_logfile'] in os.listdir(logfolder):
                ace_logfolders.append(logfolder)
    for logfolder in unknown_logfolders:
        if os.path.isdir(logfolder) and settings['ace_logfile'] in os.listdir(logfolder):
                ace_logfolders.append(logfolder)
    return mbrrl_logfolders, ace_logfolders


# logfolders is solely dependent on folders and thus is an optional argument
# provide logfolders in meta_batch_plot.py so that we can call batch_plot.py with subprocess to free up memory
def run(folders, module = None):
    if module:
        if 'plot_settings' not in module:
            module = 'plot_settings_' + module
        imported = importlib.import_module(module)
        settings.update(imported.settings)
        folders = settings['folders_to_analyse']
        if 'fontsize' in settings['plot_settings']:
            plt.rcParams.update({'font.size': settings['plot_settings']['fontsize']})
        if 'linestyles' in settings['plot_settings']:
            aysT.init_cycler(settings['plot_settings']['linestyles'])                   # this has to be done here rather than in a loop as it increases RAM usage alot!
    if not folders:
        print('No folders are defined')
        return

    logfolders, ace_logfolders = get_logfolders(folders)
    if logfolders == []:
        logfolders = folders
    
    if len(folders) == 1:
        base_folder = folders[0]
    else:
        base_folder = get_common_folder(folders)
        if base_folder == '' or not base_folder:
            base_folder = folders[0]
    base_folder = base_folder[:200] if len(base_folder) > 200 else base_folder
    print("Base Folder: " + base_folder)
    
    if settings['is_rpg']:
        print('Results are RPG, do not group by instances')
        for po in settings['plot_options']:
            po.append('is_rpg')

    # analyse by domains to prevent excessive memory usage
    domain_folders = {}
    for folder in logfolders:
        if not os.path.isdir(folder):
            continue
        print("Reading " + folder + "...")
        domain, planner, policy = parser.interpret_name( folder[folder.rfind('/')+1:-1] )
        if not any(['domain' in grouping_key for grouping_key in settings['grouping_keys']]):
            domain = 'alldomain'
        if domain is None:
            print("Skip invalid folder - missing domain (check that PLANNERS and POLICIES in parser.py are defined correctly")
            continue
        if  planner is None:
            print("Skip invalid folder - missing planner (check that PLANNERS and POLICIES in parser.py are defined correctly")
            continue
        if settings['domains']:
            if domain not in settings['domains']:
                print("Skip domain " + domain)
                continue
        if settings['planners']:
            if planner not in settings['planners']:
                print("Skip planner " + planner)
                continue
        if settings['policies']:
            if policy not in settings['policies']:
                print("Skip policy " + policy)
                continue
        if settings['quick_plotting'] and settings['quick_plotting'] > 0:
            try:
                num = int(folder[folder.rfind('_')+1 :])
                if num % settings['quick_plotting'] != 0:
                    print("Skip folder because its number (" + str(num) + ") is not a multiple of " + str(settings['quick_plotting']))
                    continue
            except ValueError:
                pass
        if domain not in domain_folders:
            domain_folders[domain] = [(folder, False)]
        else:
            domain_folders[domain].append((folder, False))

    for folder in ace_logfolders:
        if not os.path.isdir(folder):
            continue
        print("Reading " + folder + "...")
        domain = 'blocksworld'
        if domain not in domain_folders:
            domain_folders[domain] = [(folder, True)]
        else:
            domain_folders[domain].append((folder, True))

    if not domain_folders:
        raise Exception('No valid folders to plot')

    # analyse by domain, then clear the data
    for domain, folders in domain_folders.items():
        analyses = {}
        for folder, is_ACE in folders:
            print("Reading " + folder + "...")
            if domain not in analyses:
                analyses[domain] = []
            verbose = 1
            try:
                if is_ACE:
                    analysis = parser.parse_ace_results(folder.strip()+'/'+settings['ace_logfile'], verbose)
                else:
                    analysis = parser.parse_mbrrl_results(folder.strip()+'/'+settings['logfile'], verbose)
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                analysis = False
            if analysis:                                # if successfully analysed results
                analyses[domain].append(analysis)
                # print("    >> Reward have dimensions ", end = '')
                # print(np.shape(analysis.get_data('rewards')[0]))
            elif verbose == 0:
                if is_ACE:
                    print("Failed to analyse " + folder.strip()+'/'+settings['ace_logfile'])
                else:
                    print("Failed to analyse " + folder.strip()+'/'+settings['logfile'])
        
        if not analyses:
            print('WARNING: Not a single folder is analysed, check that root_folder is set correctly')

        # analysing results of same domain, only works if they are in separate folders
        # otherwise, use get_grouped_data to separate them
        if not settings['grouping_keys']:
            is_grouping_data = False
            settings['grouping_keys'].append([])        # at least have 1 empty element, that is, no grouping used
        else:
            is_grouping_data = True

        for domain in analyses:                         # for analyse belonging to the same domain
            fig_path = base_folder+'/fig_'+domain
            fc_index = 0
            for fc in settings['filter_conditions']:
                analyses_of_interest = [a for a in analyses[domain] if pass_filter(a, fc)]
                if not analyses_of_interest and fc:
                    print('No analyses from domain \'' + domain + '\' fit filter condition #' + str(fc_index))
                    fc_index += 1
                    continue
                num_str = aysT.gen_num(fig_path) if not is_grouping_data else ""
                multi_analysis = aysT.MultiAnalysis(analyses_of_interest, logfolder = fig_path+'/'+num_str)
                fc_index += 1

                for grouping_key in settings['grouping_keys']:
                    group_fig_path = aysT.list2string(lsof_strings=grouping_key, sort=True, linebreak=False, delimiter='_')
                    num_str = aysT.gen_num(fig_path, group_fig_path)
                    multi_analyses = []
                    if grouping_key:
                        # now we split the analyses further into those of the same values for attirbutes listed in settings['grouping_keys']
                        # parameters used to split into groups of analyses with the same identifier
                        kwargs = {'identifier': grouping_key}
                        lsof_grouped_analyses = multi_analysis.get_grouped_data(multi_analysis.analyses, **kwargs)
                        # for each grouped analyse, create a MultiAnalysis object
                        for group_analyses in lsof_grouped_analyses:
                            multi_analyses.append(aysT.MultiAnalysis(
                                group_analyses, 
                                logfolder = fig_path+'/'+group_fig_path+'_'+num_str,
                                identifier = grouping_key))
                    else:
                        multi_analyses = [multi_analysis]
                    plot_argv = [po+settings['generic_plot_options'] for po in settings['plot_options']]
                    for ma in multi_analyses:
                        ma.plot(settings.get('delete_grouping_keys', []), plot_argv, **settings['plot_settings'])
                        if 'save' in settings['generic_plot_options']:
                            print('Saving figures in ' + ma.logfolder)

        analyses.clear()        # clear memory



if __name__ == "__main__":
    # this generates a figure with all the legends stylelines
    # aysT.generate_all_legend_styles(mbrrl_path+'/all_legends.png')
    module = None
    if len(sys.argv) >= 2:
        for i in range(1, len(sys.argv)):
            if ('/' in sys.argv[i]):                        # assume absolute folder path is given
                settings['folders_to_analyse'].append(sys.argv[i])
            else:
                try:
                    int(sys.argv[i])                        # input is an int
                    settings['folders_to_analyse'].append(mbrrl_path+'/results-' + sys.argv[i])
                except ValueError:
                    module = sys.argv[i]
    run(folders = settings['folders_to_analyse'], module = module)