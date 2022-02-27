#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:46:20 2019

@author: alvin
"""

# ----- GENERAL SETTINGS ----- #
num_reps = 1                # num of rounds per instance
save_log = True             # True: save console file

# ----- DOMAINS ----- #
domains = ['tiago_hri']

# ----- LEARNER ----- #
learners = ['lfit']

# ----- TRANSITIONS ----- #
transitions_files = {
	# 'tiago_hri': ['transitions/transitions_all_1.dat', 'transitions/transitions_all_2.dat', 'transitions/transitions_all_3.dat', 'transitions/transitions_all_4.dat', 'transitions/transitions_all_5.dat', 'transitions/transitions_all_6.dat', 'transitions/transitions_all_7.dat', 'transitions/transitions_all_8.dat', 'transitions/transitions_all_9.dat', 'transitions/transitions_all_10.dat'],
	# 'tiago_hri': ['transitions_TRUNCATED/transitions_all_1.dat', 'transitions_TRUNCATED/transitions_all_2.dat', 'transitions_TRUNCATED/transitions_all_3.dat', 'transitions_TRUNCATED/transitions_all_4.dat', 'transitions_TRUNCATED/transitions_all_5.dat', 'transitions_TRUNCATED/transitions_all_6.dat', 'transitions_TRUNCATED/transitions_all_7.dat', 'transitions_TRUNCATED/transitions_all_8.dat', 'transitions_TRUNCATED/transitions_all_9.dat', 'transitions_TRUNCATED/transitions_all_10.dat'],
	'tiago_hri': ['transitions_no_robot_at_learn_from_scratch/transitions_all_1.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_2.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_3.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_4.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_5.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_6.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_7.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_8.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_9.dat', 'transitions_no_robot_at_learn_from_scratch/transitions_all_10.dat'],
	'tiago_fetch': ['transitions/transitions_all_1.dat', 'transitions/transitions_all_2.dat', 'transitions/transitions_all_3.dat', 'transitions/transitions_all_4.dat', 'transitions/transitions_all_5.dat', 'transitions/transitions_all_6.dat', 'transitions/transitions_all_7.dat', 'transitions/transitions_all_8.dat', 'transitions/transitions_all_9.dat', 'transitions/transitions_all_10.dat'],
	'turtlebot_survey': ['transitions/transitions_all_1.dat', 'transitions/transitions_all_2.dat', 'transitions/transitions_all_3.dat', 'transitions/transitions_all_4.dat', 'transitions/transitions_all_5.dat', 'transitions/transitions_all_6.dat', 'transitions/transitions_all_7.dat', 'transitions/transitions_all_8.dat', 'transitions/transitions_all_9.dat', 'transitions/transitions_all_10.dat'],
	'husky_inspection': ['transitions_all_d1_approx_0001.dat', 'transitions_all_d1_approx_0002.dat', 'transitions_all_d1_approx_0003.dat'],
	# 'recon2': ['with_ADJACENT/transitions_all_1.dat', 'with_ADJACENT/transitions_all_2.dat', 'with_ADJACENT/transitions_all_3.dat', 'with_ADJACENT/transitions_all_4.dat', 'with_ADJACENT/transitions_all_5.dat', 'with_ADJACENT/transitions_all_6.dat', 'with_ADJACENT/transitions_all_7.dat', 'with_ADJACENT/transitions_all_8.dat', 'with_ADJACENT/transitions_all_9.dat', 'with_ADJACENT/transitions_all_10.dat'],
	'recon2': ['transitions/transitions_all_1.dat', 'transitions/transitions_all_2.dat', 'transitions/transitions_all_3.dat', 'transitions/transitions_all_4.dat', 'transitions/transitions_all_5.dat', 'transitions/transitions_all_6.dat', 'transitions/transitions_all_7.dat', 'transitions/transitions_all_8.dat', 'transitions/transitions_all_9.dat', 'transitions/transitions_all_10.dat'],
	# 'robot_inspection': ['with_ADJACENT/transitions_all_1.dat', 'with_ADJACENT/transitions_all_2.dat', 'with_ADJACENT/transitions_all_3.dat', 'with_ADJACENT/transitions_all_4.dat', 'with_ADJACENT/transitions_all_5.dat', 'with_ADJACENT/transitions_all_6.dat', 'with_ADJACENT/transitions_all_7.dat', 'with_ADJACENT/transitions_all_8.dat', 'with_ADJACENT/transitions_all_9.dat', 'with_ADJACENT/transitions_all_10.dat']
	'robot_inspection': ['transitions/transitions_all_1.dat', 'transitions/transitions_all_2.dat', 'transitions/transitions_all_3.dat', 'transitions/transitions_all_4.dat', 'transitions/transitions_all_5.dat', 'transitions/transitions_all_6.dat', 'transitions/transitions_all_7.dat', 'transitions/transitions_all_8.dat', 'transitions/transitions_all_9.dat', 'transitions/transitions_all_10.dat']
}

actions = {
	'tiago_hri': None,
	'tiago_fetch': None,
	'turtlebot_survey': None,
	'husky_inspection': None,
	'robot_inspection': None,
	'recon2': None
	# 'recon2': 'move',				# learn rules for move action only
	# 'recon2': '+',				# learn rules for every action separately (separate their transitions and learn individually, then concatenate their learned rules)
}

# ----- CONFIG ----- #
configs = []
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'true',
# 	'lfit_learner_aggressive_prunning': 'true',
# 	'max_transitions_per_action': 100
# }
# configs.append(config)
config = {
	# 'lfit_learner_max_action_variables': 4,
	# 'lfit_learner_max_preconditions': 5,
	# 'lfit_learner_optimal': 'false',
	'lfit_learner_use_subsumption_tree': 'true',
	'lfit_learner_aggressive_prunning': 'true',
	'max_transitions_per_action': 500
}
configs.append(config)
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'true',
# 	'lfit_learner_aggressive_prunning': 'false',
# 	'max_transitions_per_action': 100
# }
# configs.append(config)
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'true',
# 	'lfit_learner_aggressive_prunning': 'false',
# 	'max_transitions_per_action': 500
# }
# configs.append(config)


# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'false',
# 	'lfit_learner_aggressive_prunning': 'true',
# 	'max_transitions_per_action': 100
# }
# configs.append(config)
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'false',
# 	'lfit_learner_aggressive_prunning': 'true',
# 	'max_transitions_per_action': 500
# }
# configs.append(config)
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'false',
# 	'lfit_learner_aggressive_prunning': 'false',
# 	'max_transitions_per_action': 100
# }
# configs.append(config)
# config = {
# 	# 'lfit_learner_max_action_variables': 4,
# 	# 'lfit_learner_max_preconditions': 5,
# 	# 'lfit_learner_optimal': 'false',
# 	'lfit_learner_use_subsumption_tree': 'false',
# 	'lfit_learner_aggressive_prunning': 'false',
# 	'max_transitions_per_action': 500
# }
# configs.append(config)