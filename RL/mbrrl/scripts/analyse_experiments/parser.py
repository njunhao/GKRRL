#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:53:26 2019

@author: alvin
"""

import common_utils
import gc
from enum import Enum, auto
import analysis_type as aysT
import parser_ace_prolog


PLANNERS = ['prost', 'vi', 'pi', 'qlearning', 'doubleq', 'dual-doubleq', 'ql', 'sarsa', 'sarsal', 'rmax', 'vmax', 'dynaq', 'dyna2', 'ps']
POLICIES = ['greedy', 'epsilon', 'softmax', 'thompson', 'thompson-ucb', 'ucb', 'random', 'import']
PERFORM_TIMESTEP_CORRECTION = False                                  # set to True if timestamp continues to be incremented with noop() at terminal states


class MSG_TYPE(Enum):
    DOMAIN = auto()
    INSTANCE_NAME = auto()
    PARSER = auto()
    INITIAL_DOMAIN = auto()
    LATENT_OBJECTS = auto()
    DYANMIC_CONSTRAINTS = auto()
    LEARNER = auto()
    LEARN_FROM_FAILURE = auto()
    USE_MODEL = auto()
    MODEL_REPRESENTATION = auto()
    EXPERIENCE = auto()
    FA = auto()
    FA_DUAL = auto()
    ELIGIBILITY = auto()
    RMAX = auto()
    SYNC_MODEL = auto()
    REPEATED_PARAMS = auto()
    ALLOW_NOOP_ACTION = auto()
    CHECK_LOOP = auto()
    REVERT_POLICY = auto()
    REPLAY_TO_GOAL = auto()
    BEAM_WIDTH = auto()
    MULTI_PLANNING = auto()
    HYPOTHESIS_MODEL_NUM = auto()
    ROLLOUT_HORIZON = auto()
    MAX_ROUND_FOR_ML = auto()
    LOCAL_MIN = auto()
    SELF_PLAY = auto()
    MVE_HORIZON = auto()
    MQE_HORIZON = auto()
    MQTE_HORIZON = auto()
    INTRINSIC_REWARD = auto()
    ALGO_NAME = auto()
    PLANNER_DESC = auto()
    LSOF_ACTION = auto()
    LSOF_STATE = auto()
    PRECOND = auto()
    INITIAL_STATE = auto()
    EPISODE_INFO = auto()
    PLANNING_STEP = auto()
    CURR_STATE = auto()
    ACTION_TAKEN = auto()
    EXECUTION_STATUS = auto()
    REWARD_RECEIVED = auto()
    FINAL_STATE = auto()
    EPISODE_END = auto()
    EPISODE_END_REWARD = auto()
    EPISODE_END_ORIGINAL_REWARD = auto()
    TERMINAL_STATE = auto()
    EPISODE_END_STATUS = auto()
    EXECUTION_TIMESTAMP = auto()
    TIME_TAKEN = auto()
    NUM_FEATURES = auto()
    SESSION_TIME = auto()
 
MSG_TUPLE = [("Domain:", MSG_TYPE.DOMAIN.value), \
             ("Instance:", MSG_TYPE.INSTANCE_NAME.value), \
             ("Initial Domain:", MSG_TYPE.INITIAL_DOMAIN.value), \
             ("Latent Objects:", MSG_TYPE.LATENT_OBJECTS.value), \
             ("Dynamic Goal Constraints:", MSG_TYPE.DYANMIC_CONSTRAINTS.value), \
             ("Parser:", MSG_TYPE.PARSER.value), \
             ("Learner:", MSG_TYPE.LEARNER.value), \
             ("Learn From Failure:", MSG_TYPE.LEARN_FROM_FAILURE.value), \
             ("Use model to determine applicable actions:", MSG_TYPE.USE_MODEL.value), \
             ("Model Representation:", MSG_TYPE.MODEL_REPRESENTATION.value), \
             ("Experience:", MSG_TYPE.EXPERIENCE.value), \
             ("Function Approximation:", MSG_TYPE.FA.value), \
             ("Function Approximation (dual):", MSG_TYPE.FA_DUAL.value), \
             ("Eligibility Trace Type:", MSG_TYPE.ELIGIBILITY.value), \
             ("Maximum Immediate Reward:", MSG_TYPE.RMAX.value),
             ("Sync Model:", MSG_TYPE.SYNC_MODEL.value), \
             ("Repeated Params in Actions:", MSG_TYPE.REPEATED_PARAMS.value), \
             ("NOOP Actions:", MSG_TYPE.ALLOW_NOOP_ACTION.value), \
             ("Check for Loop:", MSG_TYPE.CHECK_LOOP.value), \
             ("Revert to Best Policy", MSG_TYPE.REVERT_POLICY.value), \
             ("Replay Trajectory to Goal:", MSG_TYPE.REPLAY_TO_GOAL.value), \
             ("Beam Search:", MSG_TYPE.BEAM_WIDTH.value), \
             ("Multi-Planning Strategy:", MSG_TYPE.MULTI_PLANNING.value), \
             ("Num of Hypothesis Domains:", MSG_TYPE.HYPOTHESIS_MODEL_NUM.value), \
             ("Rollout Horizon:", MSG_TYPE.ROLLOUT_HORIZON.value), \
             ("Max Round for Model Learning:", MSG_TYPE.MAX_ROUND_FOR_ML.value), \
             ("Local Minimum Detection:", MSG_TYPE.LOCAL_MIN.value), \
             ("Self-Play:", MSG_TYPE.SELF_PLAY.value), \
             ("MVE Horizon:", MSG_TYPE.MVE_HORIZON.value), \
             ("MQE Horizon:", MSG_TYPE.MQE_HORIZON.value), \
             ("MQTE Horizon:", MSG_TYPE.MQTE_HORIZON.value), \
             ("Intrinsic Reward:", MSG_TYPE.INTRINSIC_REWARD.value), \
             ("Planner:", MSG_TYPE.ALGO_NAME.value), \
             ("Planner Desc:", MSG_TYPE.PLANNER_DESC.value), \
             ("----------------Actions---------------", MSG_TYPE.LSOF_ACTION.value), \
             ("-----------------CPFs-----------------", MSG_TYPE.LSOF_STATE.value), \
             ("---------Action Preconditions---------", MSG_TYPE.PRECOND.value), \
             ("----------Initial State---------------", MSG_TYPE.INITIAL_STATE.value), \
             (">>> STARTING ROUND", MSG_TYPE.EPISODE_INFO.value), \
             ("Planning step", MSG_TYPE.PLANNING_STEP.value), \
             ("Current state:", MSG_TYPE.CURR_STATE.value), \
             ("Submitted action:", MSG_TYPE.ACTION_TAKEN.value), \
             ("Execution status:", MSG_TYPE.EXECUTION_STATUS.value), \
             ("Immediate reward:", MSG_TYPE.REWARD_RECEIVED.value), \
             ("Final state:", MSG_TYPE.FINAL_STATE.value), \
             (">>> END OF ROUND", MSG_TYPE.EPISODE_END.value), \
             ("Immediate Rewards:", MSG_TYPE.EPISODE_END_REWARD.value), \
             ("Original Immediate Rewards:", MSG_TYPE.EPISODE_END_ORIGINAL_REWARD.value), \
             ("Terminal Status (0=no goal, 1=goal, -1=deadend):", MSG_TYPE.TERMINAL_STATE.value), \
             ("Execution Status (0=failure, 1=executed):", MSG_TYPE.EPISODE_END_STATUS.value), \
             ("Execution Timestamp (seconds):", MSG_TYPE.EXECUTION_TIMESTAMP.value), \
             ("Time Taken Per Round:", MSG_TYPE.TIME_TAKEN.value), \
             ("Number of Features Per Round:", MSG_TYPE.NUM_FEATURES.value), \
             (">>> Time taken for session", MSG_TYPE.SESSION_TIME.value)]


# parse logfile from ACE Prolog
def parse_ace_results(logfile, verbose = False):
    # ACE_results is list of (episode, reward, avg num of actions)
    ACE_results, runtime = parser_ace_prolog.parse_results(logfile, verbose)
    analysis = aysT.Analysis(logfile)
    analysis.set_attribute('logfolder', logfile[:logfile.rfind(os.sep)])
    analysis.set_attribute('domain', 'blocksworld_mdp')
    rpg_instance = ''
    try:
        rpg_instance = '_' + str(int(common_utils.get_filename(analysis.get_attribute('logfolder')[0]))-1)
    except:
        pass
    # algorithm and problem instance depends on directory path
    if '-STACK' in logfile:
        analysis.set_attribute('instance', 'blocksworld_inst_mdp__stack10'+rpg_instance)
    elif '-UNSTACK' in logfile:
        analysis.set_attribute('instance', 'blocksworld_inst_mdp__unstack10'+rpg_instance)
    elif '-ON' in logfile:
        analysis.set_attribute('instance', 'blocksworld_inst_mdp__on10'+rpg_instance)
    else:
        analysis.set_attribute('instance', 'blocksworld_inst_mdp__10'+rpg_instance)
        print('Warning: Unable to determine problem instance for ' + logfile)
    if '-TG-' in logfile:
        analysis.set_algorithm_type('Planner: TG')
    elif '-RIBC-' in logfile:
        analysis.set_algorithm_type('Planner: RIBC')
    elif '-KBR-' in logfile:
        analysis.set_algorithm_type('Planner: KBR')
    else:
        analysis.set_algorithm_type('Planner: Q-RRL')
        print('Warning: Unable to determine algorithm for ' + logfile)
    num_steps = 30                                                                  # TODO: this is hardcoded
    rewards_received = []
    terminal_states_per_round = []
    for episode, reward, avg_num_of_actions in ACE_results:
        rewards_for_episode = [0.0]*num_steps
        if avg_num_of_actions > 0:
            rewards_for_episode[int(avg_num_of_actions)-1] = reward                 # TODO: reward should not be at last time step, do not plot over time steps, only over episodes
        rewards_received.append(rewards_for_episode)
        if reward > 0:
            terminal_states_per_round.append(1)
        else:
            terminal_states_per_round.append(0)
    rewards_received = [rewards_received]
    execution_statuses = [[len(rewards_received[0][0]) * [True]] * len(rewards_received[0])] * len(rewards_received)
    execution_timestamp_per_round = len(ACE_results) * [0.0]
    if len(ACE_results) > 1 and ACE_results[1][0] - ACE_results[0][0] > 1:
        episodes = [v[0] for v in ACE_results]
    else:
        episodes = []
    analysis.finish(rewards_received = rewards_received, \
                    original_rewards_received = rewards_received, \
                    execution_statuses = execution_statuses, \
                    execution_timestamp = execution_timestamp_per_round, \
                    terminal_states_per_round = terminal_states_per_round, \
                    episodes = episodes)
#        raise Exception('Episode cannot increment by more than one')
    return analysis


# parse logfile from mbrrl
def parse_mbrrl_results(logfile, verbose = False):
    DEBUG = False
    episode_id = 1
    step_id = 1
    round_id = 1
    pre_state = None
    action_taken = None
    execution_status = None
    post_state = None
    reward_received = None
    rewards_received = []
    original_rewards_received = []
    execution_statuses = []
    terminal_states_per_round = []
    execution_timestamp = []
    execution_timestamp_per_round = []
    computation_time_per_round = []
    num_features_per_round = []
    analysis = aysT.Analysis(logfile)
    num_headers = 0
    num_ends = 0
    session_num = 0
    
    try:
        if verbose > 1:
            print("Parsing file " + logfile)
        file = open(logfile, "r")
    except IOError:
        if verbose > 0:
            print(logfile + " does not exist")
        return False
    line_num = 0
    for line in file:
        line_num += 1
        if not line or line == "\n":
            continue
        msg_type = parse_msg_type(line)
        if msg_type == None:
            continue
        elif msg_type == MSG_TYPE.DOMAIN.value:
            analysis.set_attribute('domain', line[line.find(": ")+2:].strip())
            num_headers += 1
        elif msg_type == MSG_TYPE.ALGO_NAME.value:
            analysis.set_algorithm_type(line)
            if DEBUG:
                print(analysis.print_algorithm())
        elif msg_type == MSG_TYPE.PLANNER_DESC.value:
            line = line[line.find('[')+1 : line.find(']')]
            key_w_values = line.split(' -')
            for key_w_value in key_w_values:
                key_w_value = key_w_value.strip()
                key_and_value = key_w_value.split(' ')
                if len(key_and_value) == 2:
                    if 'import' in key_and_value[0]:
                        analysis.set_attribute(key_and_value[0], True)              # set to true rather than file path from which it is imported
                    else:
                        analysis.set_attribute(key_and_value[0], key_and_value[1])
        elif msg_type == MSG_TYPE.INSTANCE_NAME.value:
            analysis.set_attribute('instance', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.PARSER.value:
            value = line[line.find(": ")+2:].strip()
            analysis.set_attribute('parser_file', value)
            analysis.set_attribute('parser_file', value)
            if value.find('simple') != -1:
                analysis.set_attribute('parser', 'NoPrune')
            else:
                analysis.set_attribute('parser', 'Prune')
            analysis.set_attribute('computation_hardware', 'unknown')
        elif msg_type == MSG_TYPE.INITIAL_DOMAIN.value:
            value = line[line.find(": ")+2:].strip().lower()
            analysis.set_attribute('initial_domain_file', value)                                        # initial_domain_file is unused variable
            if analysis.get_attribute('initial_domain', 1):
                analysis.set_attribute('initial_domain', analysis.get_attribute('initial_domain', 1))   # use previously defined value
            elif value.find('empty') != -1:
                analysis.set_attribute('initial_domain', 'empty')
            elif value.find('approx') != -1:
                analysis.set_attribute('initial_domain', 'approx')
            elif value.find('truth') != -1:
                analysis.set_attribute('initial_domain', 'ground-truth')
            elif value.find('deterministic') != -1:
                analysis.set_attribute('initial_domain', 'deterministic')
            elif value.find('learn') != -1:
                analysis.set_attribute('initial_domain', 'learned')
            elif value.find('latent') != -1:
                analysis.set_attribute('initial_domain', 'latent')
            else:
                analysis.set_attribute('initial_domain', 'import')
        elif msg_type == MSG_TYPE.LATENT_OBJECTS.value:
            if line[line.find(": ")+2:].strip().lower() == 'yes':
                analysis.set_attribute('latent_objects', True)                                          # if false, then don't add attribute to be compatible with older logs which does not have this attribute
        elif msg_type == MSG_TYPE.DYANMIC_CONSTRAINTS.value:
            value = float(line[line.find(": ")+2:].strip())
            if value != 0.0:
                analysis.set_attribute('dynamic_constraints', value)                                    # if value = 0, then don't add attribute to be compatible with older logs which does not have this attribute
        elif msg_type == MSG_TYPE.LEARNER.value:
            analysis.set_attribute('learner', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.LEARN_FROM_FAILURE.value:
            if line[line.find(": ")+2:].strip().lower() == 'disabled':
            	analysis.set_attribute('learn_from_failure', False)
            else:
            	analysis.set_attribute('learn_from_failure', line[line.find(": ")+2 :  line.find("(")].strip())
        elif msg_type == MSG_TYPE.USE_MODEL.value:
            value = line[line.find(": ")+2:].strip().lower()
            analysis.set_attribute('use_model_to_check_applicable_action', value)
        elif msg_type == MSG_TYPE.MODEL_REPRESENTATION.value:
            value = line[line.find(": ")+2:].strip().lower()
            analysis.set_attribute('model_representation', value)
        elif msg_type == MSG_TYPE.EXPERIENCE.value:
            value = line[line.find(": ")+2:].strip().lower()
            analysis.set_attribute('experience', value)
        elif msg_type == MSG_TYPE.FA.value or msg_type == MSG_TYPE.FA_DUAL.value:
            if msg_type == MSG_TYPE.FA_DUAL.value:
                # clear values set previously when msg_type == MSG_TYPE.FA.value
                analysis.set_attribute('function_approximation', None)
                analysis.set_attribute('function_approximation_feature_selection', None)
                analysis.set_attribute('function_approximation_feature_selection_mod', None)
                analysis.set_attribute('function_approximation_context', None)
                analysis.set_attribute('function_approximation_max_criteria', None)
                analysis.set_attribute('features_learner', None)
                analysis.set_attribute('features_learner_sync_learning', None)
                analysis.set_attribute('features_learner_zeta', None)
                analysis.set_attribute('features_learner_initial_feature_size', None)
                analysis.set_attribute('features_learner_max_feature_size', None)
                analysis.set_attribute('features_learner_tau', None)

            value = line[line.find(": ")+2:].strip()
            values = value.split('~')                       # FA and Feature Learner is delimited by ~
            if 'lfa' in values[0].lower():
                value = values[0].strip()
                value = value.replace('null', 'Null')
                value = value.replace('ground', 'Gnd')
                value = value.replace('location', 'Loc')
                value = value.replace('goal', 'Goal')
                value = value.replace('given-ordered', 'GO')
                value = value.replace('ordered', 'O')
                value = value.replace('proximity', 'PX')
                value = value.replace('synergy', 'S')
                value = value.replace('all', 'A')
                if '(' in value:
                    values_ = value[: value.find('(')]
                else:
                    values_ = value
                values_ = values_.replace('_', '-').split('-')
                analysis.set_attribute('function_approximation', values_[0].strip())
                if len(values_) > 2:
                    analysis.set_attribute('function_approximation_feature_selection', values_[1].strip())
                    analysis.set_attribute('function_approximation_feature_selection_mod', values_[-1].strip())
                
                if '(' in value and ')' in value:
                    value = value[value.find('(')+1 :].replace(')', '').strip()
                    for v in value.split(','):
                        if 'CX' in v:
                            v = v.strip()
                            if v[-1] == '-':
                                v = v[:-1]
                            analysis.set_attribute('function_approximation_context', v.strip())
                        else:
                            analysis.set_attribute('function_approximation_max_criteria', v.strip())
                
                if len(values) > 1:
                    value = values[1].strip()
                    analysis.set_attribute('features_learner', value[: value.find('(')].strip())
                    values_ = [v.strip() for v in value[value.find('(')+1 :].replace(')', '').split(',')]
                    for value in values_:
                        if value == 'SL':
                            analysis.set_attribute('features_learner_sync_learning', 'SL')
                        elif value == 'DSL':
                            analysis.set_attribute('features_learner_sync_learning', 'DSL')
                        else:
                            v = value[value.find('=')+1 :].strip()
                            if 'zeta' in value:
                                analysis.set_attribute('features_learner_zeta', v)
                            elif 'Initial Feature Size' in value:
                                analysis.set_attribute('features_learner_initial_feature_size', v)
                            elif 'Max Feature Size' in value:
                                analysis.set_attribute('features_learner_max_feature_size', v)
                            elif 'Max Addition' in value:
                                analysis.set_attribute('features_learner_tau', v)
                else:
                    analysis.set_attribute('features_learner', None)
            else:
                analysis.set_attribute('function_approximation', value)
                analysis.set_attribute('features_learner', None)
        elif msg_type == MSG_TYPE.ELIGIBILITY.value:
            analysis.set_attribute('eligibility_trace_type', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.RMAX.value:
            analysis.set_attribute('rmax', float(line[line.find(": ")+2:].strip()))
        elif msg_type == MSG_TYPE.SYNC_MODEL.value:
            analysis.set_attribute('sync_model', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.REPEATED_PARAMS.value:
            value = line[line.find(": ")+2:].strip().lower() != 'disabled'
            analysis.set_attribute('allow_repeated_params', value)
        elif msg_type == MSG_TYPE.ALLOW_NOOP_ACTION.value:
            value = line[line.find(": ")+2:].strip().lower().find('disabled') == -1
            analysis.set_attribute('allow_noop_actions', value)
            value = line[line.find(": ")+2:].strip().lower().find('zero reward') == -1
            analysis.set_attribute('allow_noop_reward', value)
        elif msg_type == MSG_TYPE.CHECK_LOOP.value:
            value = line[line.find(": ")+2:].strip()
            try:
                value = int(value)
                if value <= 0:
                    analysis.set_attribute('loop_detection', 'disabled')
                else:
                    analysis.set_attribute('loop_detection', value)
            except:
                analysis.set_attribute('loop_detection', 'disabled')
        elif msg_type == MSG_TYPE.REVERT_POLICY.value:
            value = line[line.find(": ")+2:].strip().lower() != 'disabled'
            analysis.set_attribute('revert_to_best_policy', value)
        elif msg_type == MSG_TYPE.REPLAY_TO_GOAL.value:
            value = line[line.find(": ")+2:].strip().lower() != 'disabled'
            analysis.set_attribute('replay_trajectory_to_goal', value)
        elif msg_type == MSG_TYPE.BEAM_WIDTH.value:
            analysis.set_attribute('beam_search_branch', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.MULTI_PLANNING.value:
            value = line[line.find(": ")+2:].strip()
            if value.lower() == 'None':
                value = 'disabled'
            analysis.set_attribute('multi_planning', value)
        elif msg_type == MSG_TYPE.HYPOTHESIS_MODEL_NUM.value:
            analysis.set_attribute('num_hypothesis_domains', int(line[line.find(": ")+2:].strip()))
        elif msg_type == MSG_TYPE.ROLLOUT_HORIZON.value:
            analysis.set_attribute('rollout_horizon', line[line.find(": ")+2:].strip())
        elif msg_type == MSG_TYPE.MAX_ROUND_FOR_ML.value:
            value = line[line.find(": ")+2:].strip()
            try:
                value = int(value)
                if value < 0:
                    analysis.set_attribute('max_round_for_ml', 'disabled')
                else:
                    analysis.set_attribute('max_round_for_ml', value)
            except:
                analysis.set_attribute('max_round_for_ml', 'disabled')
        elif msg_type == MSG_TYPE.LOCAL_MIN.value:
            value = line[line.find(": ")+2:].strip()
            if value.lower() == 'disabled':
                analysis.set_attribute('local_min_detection', 'disabled')
            else:
                analysis.set_attribute('local_min_detection', '{'+value+'}')
        elif msg_type == MSG_TYPE.SELF_PLAY.value:
            value = line[line.find(": ")+2:].strip()
            if value.lower() == 'disabled':
                analysis.set_attribute('self_play', 'disabled')
            else:
                analysis.set_attribute('self_play', '{'+value+'}')
        elif msg_type == MSG_TYPE.MVE_HORIZON.value:
            value = line[line.find(": ")+2:].strip()
            analysis.set_attribute('mve_horizon', int(value))
        elif msg_type == MSG_TYPE.MQTE_HORIZON.value or msg_type == MSG_TYPE.MQE_HORIZON.value:
            value = line[line.find(": ")+2:].strip()
            analysis.set_attribute('mqte_horizon', int(value))
        elif msg_type == MSG_TYPE.INTRINSIC_REWARD.value:
            value = line[line.find(": ")+2:].strip()
            if value.lower() == 'disabled':
                analysis.set_attribute('intrinsic_reward', 'disabled')
            else:
                beta = ''
                beta_decay = ''
                rmax = ''
#                experience_type = ''
                aggregation = ''                                                             # TODO: default is average if not stated
                if '(' in value:
                    params = value[value.find('(')+1:-1].strip().split(',')
                    for param in params:
                        param = param.strip()
                        if 'Rmax' in param:
                            rmax = param[param.find("=")+1:].strip()
                        elif 'beta-decay' in param:
                            beta_decay = param[param.find("=")+1:].strip()
                        elif 'beta' in param:
                            beta = param[param.find("=")+1:].strip()
                        else:
                            if 'relational' in param:
#                                experience_type = param[param.find("=")+1:].strip()
                                param = param.replace('relational', '')
                            aggregation = param.strip()
                    value = common_utils.list2string(value[: value.find('(')].strip().split(', '), sort = True, linebreak = False, delimiter = '+')   # if combination of intrinsic, sort them
                if aggregation == '':
                    aggregation = 'average'                                                             # TODO: default is average if not stated
                analysis.set_attribute('intrinsic_reward', value)
                analysis.set_attribute('intrinsic_reward_rmax', rmax)
                analysis.set_attribute('intrinsic_reward_beta', beta)
                analysis.set_attribute('intrinsic_reward_beta_decay', beta_decay)
                # analysis.set_attribute('intrinsic_reward_experience', experience_type)
                analysis.set_attribute('intrinsic_reward_aggregation', aggregation)
        elif msg_type == MSG_TYPE.LSOF_ACTION.value:
            analysis.set_lsof_actions(file)
            if DEBUG:
                print(analysis.print_lsof_actions(0))   # quick-hack: this will print last element
        elif msg_type == MSG_TYPE.LSOF_STATE.value:
            analysis.set_lsof_states(file)
            if DEBUG:
                print(analysis.print_lsof_states(0))    # quick-hack: this will print last element
        elif msg_type == MSG_TYPE.PRECOND.value:
            analysis.parse_precond(file)
        elif msg_type == MSG_TYPE.INITIAL_STATE.value:
            analysis.set_initial_state(file)
            if DEBUG:
                print(analysis.print_initial_state(0))  # quick-hack: this will print last element
            pre_state = analysis.get_initial_state(0)
        elif msg_type == MSG_TYPE.EPISODE_INFO.value:
            pass  # nothing to do
        elif msg_type == MSG_TYPE.PLANNING_STEP.value:
            (episode_id, round_id, step_id) = analysis.parse_counter(line)
        elif msg_type == MSG_TYPE.CURR_STATE.value:
            if step_id == 1:
                post_state = None
            else:
                post_state = analysis.parse_state(file, True, line)
                if not post_state:
                    continue
                analysis.add_transition(pre_state, action_taken, post_state, reward_received, execution_status, episode_id, round_id, step_id-1)
                pre_state = post_state
                if DEBUG:
                    print(analysis.print_transitions(episode_id, step_id-1))
        elif msg_type == MSG_TYPE.ACTION_TAKEN.value:
            action_taken = analysis.parse_action_taken(line)
        elif msg_type == MSG_TYPE.EXECUTION_STATUS.value:
            execution_status = analysis.parse_execution_status(line)
        elif msg_type == MSG_TYPE.REWARD_RECEIVED.value:
            reward_received = analysis.parse_reward_received(line)
        elif msg_type == MSG_TYPE.FINAL_STATE.value:
                post_state = analysis.parse_state(file, True, line)
                analysis.add_transition(pre_state, action_taken, post_state, reward_received, execution_status, episode_id, round_id, step_id)
                if DEBUG:
                    print(analysis.print_transitions(episode_id, step_id-1))
        elif msg_type == MSG_TYPE.EPISODE_END.value:
            analysis.set_episode_reward(line)
        elif msg_type == MSG_TYPE.EPISODE_END_REWARD.value:
            rewards_received.append(analysis.parse_string_of_numbers(file))
        elif msg_type == MSG_TYPE.EPISODE_END_ORIGINAL_REWARD.value:
            original_rewards_received.append(analysis.parse_string_of_numbers(file))
        elif msg_type == MSG_TYPE.EPISODE_END_STATUS.value:
            execution_statuses.append(analysis.parse_execution_statuses(file))
        elif msg_type == MSG_TYPE.TERMINAL_STATE.value:
            terminal_states_per_round += analysis.parse_round_information(file)
        elif msg_type == MSG_TYPE.EXECUTION_TIMESTAMP.value:
            if PERFORM_TIMESTEP_CORRECTION:
                execution_timestamp.append(analysis.parse_string_of_numbers(file))
            else:
                execution_timestamp_per_round += [float(value[-1]) for value in analysis.parse_string_of_numbers(file)]
        elif msg_type == MSG_TYPE.TIME_TAKEN.value:
            computation_time_per_round += analysis.parse_round_information(file)
        elif msg_type == MSG_TYPE.NUM_FEATURES.value:
            num_features_per_round += analysis.parse_round_information(file)
        elif msg_type == MSG_TYPE.SESSION_TIME.value:
            session_num += 1
            analysis.set_time_taken(line)
            num_ends += 1
            if session_num == 1000:
                break
    
    file.close()

    if line_num == 0 or num_headers == 0 or num_ends == 0 or num_headers != num_ends:   # empty or incomplete logfile
        if verbose > 0:
            msg = "Failed to parse " + logfile
            if line_num == 0:
                msg = msg + " - empty logfile"
            if num_headers < num_ends or num_headers == 0:
                msg = msg + " - no header"
            if num_headers > num_ends or num_ends == 0:
                msg = msg + " - no timestamp at EOF"
            print(msg)
        return False

    if original_rewards_received == []:
        original_rewards_received = rewards_received
    if execution_statuses == []:                                                # if logfile did not have this, then assume all are successful executions
        execution_statuses = [[len(rewards_received[0][0]) * [True]] * len(rewards_received[0])] * len(rewards_received)
    if execution_timestamp_per_round == []:                                     # if logfile did not have this, then assume no duration
        execution_timestamp_per_round = len(terminal_states_per_round) * [0.0]
    if PERFORM_TIMESTEP_CORRECTION:
        for execution_timestep_in_session, rewards_received_in_session in zip(execution_timestamp, rewards_received):
                for execution_timestep_in_round, rewards_received_in_round in zip(execution_timestep_in_session, rewards_received_in_session):
                    if '0' in rewards_received_in_round:
                        # terminal state reached, timestamp stops at terminal state, not at last step
                        execution_timestamp_per_round += [float(execution_timestep_in_round[rewards_received_in_round.index('0')-1])]
                    else:
                        # terminal state not reached, timestamp stops at last step
                        execution_timestamp_per_round += [float(execution_timestep_in_round[-1])]
    analysis.finish(rewards_received = rewards_received, \
                    original_rewards_received = original_rewards_received, \
                    execution_statuses = execution_statuses, \
                    execution_timestamp = execution_timestamp_per_round, \
                    terminal_states_per_round = terminal_states_per_round, \
                    computation_time_per_round = computation_time_per_round, \
                    num_features_per_round = num_features_per_round)
    # print("Finished analysing Instance/s: " + analysis.print_attribute('instance') + ", " + analysis.algorithm.get_settings())
    del pre_state
    del action_taken
    del execution_status
    del post_state
    del reward_received
    del rewards_received
    del original_rewards_received
    del execution_statuses
    del terminal_states_per_round
    del execution_timestamp
    del execution_timestamp_per_round
    del computation_time_per_round
    del num_features_per_round
    del num_headers
    del num_ends
    del session_num
    gc.collect()
    return analysis


def parse_msg_type(line):
    line = line.lower()
    for phrase, msg_type in MSG_TUPLE:
        phrase = phrase.lower()
        if line.find(phrase) == 0:
            return msg_type
    return None


def interpret_name(folderName):
    policy = None
    planner = None
    instance = None
    phrases = folderName.split('_')
    if phrases[0] == 'experiment':
        instance = phrases[1]
        if phrases[-2] in POLICIES:
            policy = phrases[-2]
            planner = phrases[-3]
            for phrase in phrases[2:-3]:
                instance = instance + '_' + phrase
        elif phrases[-2] in PLANNERS:
            planner = phrases[-2]
            for phrase in phrases[2:-2]:
                instance = instance + '_' + phrase
    return instance, planner, policy