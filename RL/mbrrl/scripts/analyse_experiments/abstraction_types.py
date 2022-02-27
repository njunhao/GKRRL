#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin
"""

import numpy as np
import re
import gc


def getPolicyName(policy):
    if policy.lower() == "epsilon":
        policy = "Epsilon-Greedy"
    elif policy.lower() == "softmax":
        policy = "Softmax"
    elif policy.lower() == "thompson":
        policy = "Thompson Sampling"
    elif policy.lower() == "thompson-ucb":
        policy = "Thompson Sampling-UCB"
    elif policy.lower() == "ucb":
        policy = "UCB"
    else:
        policy = policy.capitalize()
    return policy


class StateFluent:
    def __init__(self, fluent, index, is_deterministic, value, formulas):
        self.fluent = fluent
        self.index = index
        self.is_deterministic = is_deterministic
        self.value = value
        self.formulas = formulas

    def get_fluent(self):
        return self.fluent

    def get_index(self):
        return self.index

    def is_deterministic(self):
        return self.is_deterministic

    def get_value(self):
        return self.value

    def get_formulas(self):
        return self.formulas

    def print(self):
        string = "State Fluent " + str(self.index)
        if self.is_deterministic:
            string += " (deterministic)"
        else:
            string += " (probabilistic)"
        string += ": " + self.fluent
        if self.value is not None:
            string += ", Value: " + str(self.value)
        i = 1
        for formula in self.formulas:
            string += "\nFormula " + str(i) + ": " + formula
            i += 1
        return string


class ActionFluent:
    def __init__(self, fluent, index, precond_index, precond = None):
        self.fluent = fluent
        self.index = index
        self.precond_index = precond_index
        self.precond = precond

    def set_precond(self, precond):
        self.precond = precond

    def get_fluent(self):
        return self.fluent

    def get_index(self):
        return self.index

    def get_precond_index(self):
        return self.precond_index

    def get_precond(self):
        return self.precond

    def print(self):
        string = "Action " + str(self.index) + ": " + self.fluent
        if self.precond is None:
            string += "\nPrecondition: None"
        else:
            string += "\nPrecondition: " + self.precond
        return string

#----------------Actions---------------
#
#Action fluents:
#changetire
#loadtire(la2a1)
#loadtire(la2a2)
#loadtire(la3a1)
#move-car(la1a1, la1a2)
#move-car(la1a1, la2a1)
#move-car(la1a2, la1a3)
#move-car(la1a2, la2a2)
#move-car(la2a1, la1a2)
#move-car(la2a1, la3a1)
#move-car(la2a2, la1a3)
#move-car(la3a1, la2a2)
#---------------
#
#Legal Action Combinations:
#noop() :
#Index : 0
#Relevant preconditions:
#---------------
#move-car(la3a1, la2a2) :
#Index : 1
#Relevant preconditions:
#---------------
#move-car(la2a2, la1a3) :
#Index : 2
#Relevant preconditions:
#---------------
#move-car(la2a1, la3a1) :
#Index : 3
#Relevant preconditions:
#---------------
#move-car(la2a1, la1a2) :
#Index : 4
#Relevant preconditions:
#---------------
#move-car(la1a2, la2a2) :
#Index : 5
#Relevant preconditions:
#---------------
#move-car(la1a2, la1a3) :
#Index : 6
#Relevant preconditions:
#---------------
#move-car(la1a1, la2a1) :
#Index : 7
#Relevant preconditions:
#---------------
#move-car(la1a1, la1a2) :
#Index : 8
#Relevant preconditions:
#---------------
#loadtire(la3a1) :
#Index : 9
#Relevant preconditions:
#---------------
#loadtire(la2a2) :
#Index : 10
#Relevant preconditions:
#---------------
#loadtire(la2a1) :
#Index : 11
#Relevant preconditions:
#---------------
#changetire :
#Index : 12
#Relevant preconditions:
#---------------
class Actions:
    def __init__(self, file):
        self.actions = []
        parse_action = True
        parse_index = False
        for line in file:
            if not line or line == "\n":
                continue   # skip empty lines
            elif "---------------" in line:
                return
            elif parse_action:
                fluent = line[0:line.find(":")-1].strip()
                parse_action = False
                parse_index = True
                index = None
                precond_index = None
            elif parse_index:
                index = int(line[line.find(": ")+2:].strip())
                parse_index = False
                parse_action = True
                self.actions.append(ActionFluent(fluent, index, precond_index))

# this is for parsing SearchEngine::printTask(out)
#    def __init__(self, file):
#        self.actions = []
#        start_parsing = False
#        parse_action = False
#        parse_index = False
#        parse_precond = False
#        for line in file:
#            if "Legal Action Combinations" in line:
#                start_parsing = True
#                parse_action = True
#            elif start_parsing and (not line or line == "\n"):
#                return
#            elif start_parsing and parse_action:
#                fluent = line[0:line.find(":")-1].strip()
#                parse_action = False
#                parse_index = True
#                index = None
#                precond_index = None
#            elif start_parsing and parse_index:
#                index = int(line[line.find(": ")+2:].strip())
#                parse_index = False
#                parse_precond = True
#            elif start_parsing and parse_precond:
#                if "Relevant preconditions" in line:
#                    continue
#                elif "Precond" in line:
#                    precond_index = int(line[len("Precond"):].strip())
#                    parse_precond = False
#                elif "---------------" in line:
#                    parse_precond = False
#                    parse_action = True
#                    self.actions.append(ActionFluent(fluent, index, precond_index))
#                    # reset just in case parsing mess up
#            elif start_parsing:
#                if "---------------" in line:
#                    parse_action = True
#                    self.actions.append(ActionFluent(fluent, index, precond_index))
#                    # reset just in case parsing mess up

    def set_action_precond(self, fluent, precond_index, precond):
        for i in range(self.get_num_actions()):
            if fluent == self.actions[i].get_fluent():
                if precond_index is not self.actions[i].get_precond_index():
                    raise Exception("Indices of action does not match")
                self.actions[i].set_precond(precond)
                return
        raise Exception("Unable to find action " + fluent + " in lsof actions")

    def get_num_actions(self):
        return len(self.actions)

    def get_index(self, fluent):
        for action_fluent in self.actions:
            if fluent == action_fluent.get_fluent():
                return action_fluent.get_index()
#        raise Exception("Action fluent " + fluent + " does not exist")

    def print(self):
        string = ""
        for action in self.actions:
            string += action.print() + "\n"
        return string


class SimpleAction:
    def __init__(self, index, fluent):
        self.index = index
        self.fluent = fluent

    def print(self):
        return "Action " + str(self.index) + ": " + self.fluent


#--------------
#hasspare
#  HashIndex: 1, deterministic, caching in vectors, Kleene caching in vectors of size 10935.
#
#  Action Hash Key Map:
#    loadtire(la3a1)  : 1
#    loadtire(la2a2)  : 2
#    loadtire(la2a1)  : 3
#    changetire  : 4
#  Formula:
#case (and changetire hasspare)  then 0
#case (or (and loadtire(la2a1) vehicle-at(la2a1) spare-in(la2a1))  (and loadtire(la2a2) vehicle-at(la2a2) spare-in(la2a2))  (and loadtire(la3a1) vehicle-at(la3a1) spare-in(la3a1)) )  then 1
#case 1 then hasspare
#
#
#  Domain: false true
#  HashKeyBase: 0: 0, 1: 2
#  KleeneHashKeyBase: 3
#
#--------------
#spare-in(la2a1)
#  HashIndex: 2, deterministic, caching in vectors, Kleene caching in vectors of size 18.
#
#  Action Hash Key Map:
#    loadtire(la2a1)  : 1
#  Formula:
#case (and loadtire(la2a1) vehicle-at(la2a1) spare-in(la2a1))  then 0
#case 1 then spare-in(la2a1)
#
#
#  Domain: false true
#  HashKeyBase: 0: 0, 1: 4
#  KleeneHashKeyBase: 9
class State:
    def __init__(self, file):
        self.states = []
        formulas = []
        parse_action = True
        parse_index = False
        for line in file:
            if not line or line == "\n":
                continue   # skip empty lines
            elif "---------------" in line:
                return
            elif parse_action:
                fluent = line.rstrip()
                parse_action = False
                parse_index = True
            elif parse_index:
                index = int(line[line.find(": ")+2 : line.find(",")])
                if "deterministic" in line:
                    is_deterministic = True
                else:
                    is_deterministic = False
                parse_index = False
                parse_action = True
                self.states.append(StateFluent(fluent, index, is_deterministic, None, formulas))
                # reset just in case parsing mess up
                fluent = None
                index = None
                is_deterministic = None

# this is for parsing SearchEngine::printTask(out)
#    def __init__(self, file):
#        self.states = []
#        formulas = []
#        parse_action = True
#        parse_index = False
#        parse_formula = False
#        for line in file:
#            if not line or line == "\n":
#                continue   # skip empty lines
#            elif "Reward CPF" in line:
#                return
#            elif parse_action:
#                fluent = line.rstrip()
#                parse_action = False
#                parse_index = True
#            elif parse_index:
#                index = int(line[line.find(": ")+2 : line.find(",")])
#                if "deterministic" in line:
#                    is_deterministic = True
#                else:
#                    is_deterministic = False
#                parse_index = False
#            elif "Formula:" in line:
#                parse_formula = True
#                continue
#            elif "--------------" in line:
#                parse_action = True
#                parse_formula = False
#                self.states.append(StateFluent(fluent, \
#                                               index, \
#                                               is_deterministic, \
#                                               None, \
#                                               formulas))
#                # reset just in case parsing mess up
#                fluent = None
#                index = None
#                is_deterministic = None
#                formulas = []
#            elif parse_formula:
#                if ":" in line:
#                    parse_formula = False
#                else:
#                    formulas.append(line.rstrip())

    def get_num_state_fluents(self):
        return self.states.size()

    def get_index(self, fluent):
        for state_fluent in self.states:
            if fluent == state_fluent.get_fluent():
                return state_fluent.get_index()
        raise Exception("State fluent " + fluent + " does not exist")

    def get_simplestate(self, fluents, values):
        if fluents is None:
            return SimpleState(range(len(values)), values)
        else:
            return SimpleState([self.get_index(fluent) for fluent in fluents], \
                            values)

    def print(self):
        string = ""
        for state in self.states:
            string += state.print() + "\n"
        return string


class SimpleState:
    def __init__(self, indices, values):
        if len(indices) == 0:
            raise("indices cannot be empty")
        self.state = np.zeros((max(indices)+1))
        for index, value in zip(indices, values):
            self.state[index] = value

    def print_compact(self):
        string = ""
        for value in self.state:
            string += str(value)
        return string

    def print(self):
        index = 0
        string = ""
        for value in self.state:
            string += "State " + str(index) + ": " + str(value) + "\n"
            index += 1
        return string


class Transition:
    def __init__(self, pre_state, action, post_state, reward, original_reward, \
                 executed, episode_id, round_id, step_id):
        self.pre_state = pre_state
        self.action = action
        self.post_state = post_state
        self.reward = reward
        self.original_reward = original_reward
        self.episode_id = episode_id
        self.round_id = round_id
        self.step_id = step_id
        self.executed = executed

    def print(self):
        string = "Pre-state: " + self.pre_state.print_compact() + "\n"
        string += self.action.print() + "\n"
        string += "Post-state: " + self.post_state.print_compact() + "\n"
        if self.executed is not None:
            if self.executed:
                string += "Executed: Yes\n"
            else:
                string += "Executed: No\n"
        string += "Reward: " + str(self.reward) + "\n"
        return string


class DataMatrix:
    def __init__(self, name, matrix, steps_per_episode = None, episodes_per_step = None, episodes = None):
        # each row represents the results of steps within a episode
        # each column represents another episode
        self.data = matrix
        self.name = name
        self.steps_per_episode = steps_per_episode
        self.episodes_per_step = episodes_per_step
        self.episodes = episodes


    def get(self, mode = None):
        if mode is None:
            return self.data, None, self.episodes
        elif "cumsum" in mode:
            if "episodewise" in mode:
                raise Exception('Column-wise cumulative sum of ' + \
                                self.name + \
                                ' does not make sense!')
            else:
                # axis = 0 --> sum across rows
                # axis = 1 --> sum across columns
                # this gives cumulative reward in each episode
                # transpose it as we want to plot steps (ie make steps become row)
                # return None for std dev as it is not sensible for cumsum operator
                if len(np.shape(self.data)) == 1:
                    return np.cumsum(self.data, axis = 0), None, self.episodes
                else:
                    return np.cumsum(self.data, axis = 1), None, self.episodes
        elif "terminal" in mode:
            # returns sum after each episode
            if len(np.shape(self.data)) == 1:
                return self.data, None, self.episodes
            else:
                return np.sum(self.data, axis = 1), None, self.episodes
        elif "avg" in mode:
            # std deviation is computed here rather than using the one in constructor
            if "episodewise" in mode:  # x axis is episode
                # returns total reward / num of steps for each episode
                if self.steps_per_episode is None:
                    raise Exception("steps_per_episode must be provided to compute average reward")
                if np.isscalar(self.steps_per_episode):
                    return np.sum(self.data, axis = 1)/self.steps_per_episode, np.std(self.data, axis = 1), self.episodes
                else:
                    return np.divide(np.sum(self.data, axis = 1), self.steps_per_episode), np.std(self.data, axis = 1), self.episodes
            else:  # x axis is Step
                # returns total reward / number of episodes for each step
                if self.episodes_per_step is None:
                    raise Exception("episodes_per_step must be provided to compute average reward")
                if np.isscalar(self.episodes_per_step):
                    return np.sum(self.data, axis = 0)/self.episodes_per_step, np.std(self.data, axis = 0), self.episodes
                else:
                    return np.divide(np.sum(self.data, axis = 0), self.episodes_per_step), np.std(self.data, axis = 0), self.episodes
        else:
            return self.data, None, self.episodes


class DataMatrices:
    def __init__(self, name, matrices, identifier, steps_per_episode = None, episodes_per_step = None, episodes = None):
        # matrices is 3D matrix: (run #, episode #, step #)
        # each depth represents a run
        # each row represents the results of steps within a episode
        # each column represents another episode
        self.name = name
        self.data = [DataMatrix(name, matrix, steps_per_episode, episodes_per_step, episodes) for matrix in matrices]
        self.identifier = identifier

    # remove_outlier is the num of min and max experiments to remove as outliers
    # if remove_outlier = 2, then 2 x 2 = 4 experiments will be removed\
    # if remove_outlier is a vector, then 1st element is num of argmin to remove, 2nd element is num of argmax to remove
    def get(self, mode = None, remove_outlier = 0):
        results = [d.get(mode) for d in self.data]
        stacked_y = [y for y, _, _ in results]
        episodes= results[0][2]
        # remove outliers
        if remove_outlier:
            if not isinstance(remove_outlier, list):
                remove_outlier = [remove_outlier, remove_outlier]
            num_outliers_to_remove = sum(remove_outlier)
            if num_outliers_to_remove > 0:
                if len(stacked_y) >= 2*num_outliers_to_remove:
                    agg_each_run = np.mean(stacked_y, axis=1)                               # get average of each run
                    if remove_outlier[0] > 0:
                        indices_argmin = agg_each_run.argsort()[:remove_outlier[0]][::-1]   # get indices of max average
                    else:
                        indices_argmin = np.array([])
                    if remove_outlier[1] > 0:
                        indices_argmax = agg_each_run.argsort()[-remove_outlier[1]:][::-1]  # get indices of min average
                    else:
                        indices_argmax = np.array([])
                    stacked_y_ = []
                    for i in range(len(stacked_y)):
                        if i not in indices_argmin and i not in indices_argmax:
                            stacked_y_.append(stacked_y[i])
                    stacked_y = stacked_y_
                else:
                    print('Unable to remove ' + str(num_outliers_to_remove) + \
                          ' outliers as length of data (' + str(len(stacked_y)) +')' + \
                          ' must be at least twice that of num. of outliers to remove')
        # aggregate over all runs
        agg_y = np.mean(stacked_y, axis=0)
        std_dev = np.std(stacked_y, axis=0)
        del results
        gc.collect()
        return stacked_y, agg_y, std_dev, episodes

    def print_identity(self):
        string = "Instance: " + self.identifier['instance'] + \
                    ", Planner: " + self.identifier['planner']
        if self.identifier['policy'] is not None:
            string += ", Policy: " + getPolicyName(self.identifier['policy'])
        return string

    def get_label(self, request = None, force = False):        # request is a list of strings specifying which attributes to return
        string = ""
        if request is None:
            request = self.identifier
        elif request == []:
            return string
        elif 'logfolder' in request and self.identifier.get('logfolder', None) is not None:
            return self.identifier['logfolder']
        elif 'instance' in request and self.identifier.get('instance', None) is not None:
            instance = self.identifier['instance']
            instance = instance[instance.find('__')+2 :]
            string += 'inst_' + instance
        if 'logfolderID' in request and self.identifier.get('logfolderID', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += self.identifier['logfolderID']
        if 'model_representation' in request and self.identifier.get('model_representation', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'MDL='+self.identifier['model_representation'].title()
        if 'experience' in request and self.identifier.get('experience', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'EXP='+self.identifier['experience'].title()
        if 'initial_domain' in request and self.identifier.get('initial_domain', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += self.identifier['initial_domain'].title()
        if 'latent_objects' in request and self.identifier.get('latent_objects', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Latent-Obj=' + str(self.identifier['latent_objects'])
        if 'dynamic_constraints' in request and self.identifier.get('dynamic_constraints', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Dyn-C=' + str(self.identifier['dynamic_constraints'])
        if 'planner' in request:
            if len(string) > 0:
                 string += ', '
            string += self.identifier['planner']
        if any(['function_approximation' in req for req in request]):
            value = self.identifier.get('function_approximation', None)
            if value or force:
                if len(string) > 0:
                     string += ', '
                if value:
                    string += 'FA='
                    first = True
                    if 'function_approximation' in request and self.identifier.get('function_approximation', None):
                        first = False
                        string += self.identifier['function_approximation']
                    if 'function_approximation_feature_selection' in request and self.identifier.get('function_approximation_feature_selection', None):
                        if first:
                            first = False
                        else:
                            string += '-'
                        string += self.identifier['function_approximation_feature_selection']
                    if 'function_approximation_feature_selection_mod' in request and self.identifier.get('function_approximation_feature_selection_mod', None):
                        if first:
                            first = False
                        else:
                            string += '_'
                        string += self.identifier['function_approximation_feature_selection_mod']
                    string += ' ('
                    first = True
                    empty_contents_in_brackets = True
                    if 'function_approximation_context' in request and self.identifier.get('function_approximation_context', None):
                        empty_contents_in_brackets = False
                        if first:
                            first = False
                        string += self.identifier['function_approximation_context']
                    if 'function_approximation_max_criteria' in request and self.identifier.get('function_approximation_max_criteria', None):
                        empty_contents_in_brackets = False
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += self.identifier['function_approximation_max_criteria']
                    string += ')'
                    if empty_contents_in_brackets:
                        string = string[: -3]       # remove brackets since no string between them
                else:
                    string += 'FA=None'
        if any(['features_learner' in req for req in request]):
            value = self.identifier.get('features_learner', None)
            if value or force:
                if len(string) > 0:
                     string += ', '
                if value:
                    string += 'FL=' + self.identifier['features_learner'] + ' ('
                    first = True
                    if 'features_learner_sync_learning' in request and self.identifier.get('features_learner_sync_learning', None):
                        if first:
                            first = False
                        string += self.identifier['features_learner_sync_learning']
                    if 'features_learner_zeta' in request and self.identifier.get('features_learner_zeta', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'zeta=' + str(self.identifier['features_learner_zeta'])
                    if 'features_learner_initial_feature_size' in request and self.identifier.get('features_learner_initial_feature_size', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'I=' + str(self.identifier['features_learner_initial_feature_size'])
                    if 'features_learner_max_feature_size' in request and self.identifier.get('features_learner_max_feature_size', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'M=' + str(self.identifier['features_learner_max_feature_size'])
                    if 'features_learner_tau' in request and self.identifier.get('features_learner_tau', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'tau=' + str(self.identifier['features_learner_tau'])
                    string += ')'
                    string = string.replace(' ()', '')
                else:
                    string += 'FL=None'
        if 'eligibility_trace_type' in request and self.identifier['eligibility_trace_type'] is not None:
            if len(string) > 0:
                 string += ', '
            string += self.identifier['eligibility_trace_type']
        if 'policy' in request and self.identifier['policy'] is not None:
            if len(string) > 0:
                 string += ', '
            string += getPolicyName(self.identifier['policy'])

        if 'alpha' in request and self.identifier['alpha'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Alpha=' + str(self.identifier['alpha'])
        if 'decay' in request and self.identifier['decay'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Decay=' + str(self.identifier['decay'])
        if 'epsilon' in request and self.identifier['epsilon'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Epsilon=' + str(self.identifier['epsilon'])
        if 'import_intrinsic_reward' in request and self.identifier['import_intrinsic_reward'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Import-Intrinsic=True'
        if 'import_qvalue' in request and self.identifier['import_qvalue'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Import-Qfunction=True'
        if 'lambda' in request and self.identifier['lambda'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Lambda=' + str(self.identifier['lambda'])
        if 'horizon' in request and self.identifier['horizon'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Horizon=' + str(self.identifier['horizon'])

        if 'discount_factor' in request and self.identifier['discount_factor'] is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Discount=' + str(self.identifier['discount_factor'])
        if 'loop_detection' in request and self.identifier.get('loop_detection', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Loop=' + str(self.identifier['loop_detection'])
        if 'replay_trajectory_to_goal' in request and self.identifier.get('replay_trajectory_to_goal', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Goal-Replay=' + str(self.identifier['replay_trajectory_to_goal'])
        if 'revert_to_best_policy' in request and self.identifier.get('revert_to_best_policy', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'Revert-Policy=' + str(self.identifier['revert_to_best_policy'])
        if 'beam_search_branch' in request and self.identifier.get('beam_search_branch', None) is not None:
            if int(self.identifier['beam_search_branch']) > 1:
                if len(string) > 0:
                     string += ', '
                string += 'Beam=' + str(self.identifier['beam_search_branch'])
        if ('rollout_horizon' in request or 'num_hypothesis_domains' in request) and \
            self.identifier.get('rollout_horizon', None) is not None and self.identifier.get('num_hypothesis_domains', None) is not None:
            if len(string) > 0:
                 string += ', '
            if int(self.identifier['num_hypothesis_domains']) > 0 and int(self.identifier['rollout_horizon']) > 0:
                string += 'Rollout=M' + str(self.identifier['num_hypothesis_domains']) + ',H' + str(self.identifier['rollout_horizon'])
                if 'multi_planning' in request and self.identifier.get('multi_planning', None) is not None:
                    string += ', MPS=' + self.identifier['multi_planning']
            else:
                string += 'HM=' + str(self.identifier['num_hypothesis_domains'])
        elif 'multi_planning' in request and self.identifier.get('multi_planning', None) is not None:
            if len(string) > 0:
                string += ', '
            string += 'MPS=' + self.identifier['multi_planning']
        if 'max_round_for_ml' in request and self.identifier.get('max_round_for_ml', None) is not None:
            if len(string) > 0:
                 string += ', '
            string += 'CUTOFF=' + str(self.identifier['max_round_for_ml'])
        if 'local_min_detection' in request and self.identifier.get('local_min_detection', None) is not None:
            if len(string) > 0:
                string += ', '
            string += 'LMD=' + self.identifier['local_min_detection']
        if any(['intrinsic_reward' in req for req in request]):
            value = self.identifier.get('intrinsic_reward', None)
            if value or force:
                if len(string) > 0:
                     string += ', '
                if value:
                    string += 'IR=' + self.identifier['intrinsic_reward'] + ' ('
                    first = True
                    if 'intrinsic_reward_rmax' in request and self.identifier.get('intrinsic_reward_rmax', None):
                        if first:
                            first = False
                        string += 'IR-Rmax=' + self.identifier['intrinsic_reward_rmax']
                    if 'intrinsic_reward_beta' in request and self.identifier.get('intrinsic_reward_beta', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'beta=' + str(self.identifier['intrinsic_reward_beta'])
                    if 'intrinsic_reward_beta_decay' in request and self.identifier.get('intrinsic_reward_beta_decay', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'beta-decay=' + str(self.identifier['intrinsic_reward_beta_decay'])
                    # if 'intrinsic_reward_experience' in request and self.identifier.get('intrinsic_reward_experience', None):
                    #     if first:
                    #         first = False
                    #     else:
                    #         string += ', '
                    #     string += 'IR-Exp=' + str(self.identifier['intrinsic_reward_experience'])
                    if 'intrinsic_reward_aggregation' in request and self.identifier.get('intrinsic_reward_aggregation', None):
                        if first:
                            first = False
                        else:
                            string += ', '
                        string += 'Agg=' + str(self.identifier['intrinsic_reward_aggregation'])
                    string += ')'
                    string = string.replace(' ()', '')
                else:
                    string += 'IR=None'
        if 'self_play' in request and self.identifier.get('self_play', None) is not None:
            if len(string) > 0:
                string += ', '
            string += 'SP=' + self.identifier['self_play']
        if 'mve_horizon' in request and self.identifier.get('mve_horizon', None) is not None:
            if len(string) > 0:
                string += ', '
            string += 'MVE=' + str(self.identifier['mve_horizon'])
        if 'mqte_horizon' in request and self.identifier.get('mqte_horizon', None) is not None:
            if len(string) > 0:
                string += ', '
            string += 'MQTE=' + str(self.identifier['mqte_horizon'])
        close_bracket = False
        if 'learner' in request:
            value = self.identifier.get('learner', 'None')
            if value and (value != 'None' or force):
                if len(string) > 0:
                    string += " ("
                    close_bracket = True
                if value != 'None':
                    string += value
                else:
                    string += 'No Model Learner'
        if 'learn_from_failure' in request:
            value = self.identifier.get('learn_from_failure', None)
            if value or force:
                if close_bracket:
                    string += ", "
                elif len(string) > 0:
                    string += " ("
                    close_bracket = True
                if isinstance(value, str):
                    string += value
                elif value:
                    string += "LfF"
                else:
                    string += "No LfF"
        if close_bracket:
            string += ")"
        
        if len(string) == 0 and not force:
            label = self.get_label(request, True)
        else:
            label = string
        if len(string) == 0 and request:
            print('No label found for the following request: ', end='')
            print(request)
            label = 'Baseline'
        if False: #label.count('=') == 1:
            return label[label.find('=')+1:]        # if only 1 attribute is included in label, remove attribute name and just keep the value (e.g FA=CPF becomes CPF)
        else:
            return label

    def get_attribute(self, key):
        return self.identifier.get(key, 'None')
    
    def get_attributes(self):
        return self.identifier
    
    def get_numeric_attribute(self, key):
        try:
            return float(self.identifier.get(key, 0))
        except:
            return 0
        
    def set_attribute(self, key, value):
        self.identifier[key] = value

def merge_DataMatrices(list_data_matrices):
    matrices = []
    for data_matrices in list_data_matrices:
        if isinstance(data_matrices, DataMatrices):
            name = data_matrices.name
            identifier = data_matrices.identifier
            for data_matrix in data_matrices.data:
                if matrices == []:
                    matrices = data_matrix.data
                else:
                    matrices = np.row_stack((matrices, data_matrix.data))
                steps_per_episode = data_matrix.steps_per_episode
                episodes_per_step = data_matrix.episodes_per_step
        else:
            raise Exception('All elements in list_data_matrices must be of instance DataMatrices')
    return DataMatrices(name, matrices, identifier, steps_per_episode, episodes_per_step)


class Algorithm_Type:
    def __init__(self, line):
        # Planner: QLearning, Discount Factor: 1, Alpha: 0.1
        phrases = re.split(", |:", line)
        is_key = True
        self.params = {}
        for phrase in phrases:
            phrase = phrase.strip().replace(' ', '_').replace('/', '~')
            if is_key:
                key = phrase.lower()
                is_key = False
            else:
                is_key = True
                if key == "planner":
                    self.params[key] = phrase
                    self.params["planners"] = [phrase]
                elif key == "policy":
                    self.params[key] = phrase
                else:
                    try:
                        self.params[key] = float(phrase)
                    except ValueError:
                        self.params[key] = phrase

    def print(self):
        return self.get_settings()

    def get_param(self, key):
        if key == "planner" and self.params.get(key, None):
            operations = [value for value in self.params.get("operations", "").split('-')]
            value = self.params[key]
            first = True
            for v in operations:
                if v:
                    if first:
                        value += '~'
                        first = False
                    value += v[0]             # append first alphabet of operations to name of planner
            return value
        return self.params.get(key, None)

    # def set_param(self, key, value):
    #     self.params[key] = value

    def get_settings(self):
        string = ""
        for key, value in self.params.items():
            string += key.title() + ": " + str(value) + ", "
        return string[:-2]


def sortMatrices(a):
    if not isinstance(a, DataMatrices):
        raise Exception('Data type must be DataMatrices')
    logfolders = a.get_attribute('logfolder')
    minNum = None
    for logfolder in logfolders:
        if isinstance(logfolder, list):
            logfolder = logfolder[0]
        try:
            lognum = int(logfolder[logfolder.rfind('_')+1 :])
            if minNum is None or lognum < minNum:
                minNum = lognum
        except:
            continue
    if minNum is None:
        return 0
    else:
        return minNum