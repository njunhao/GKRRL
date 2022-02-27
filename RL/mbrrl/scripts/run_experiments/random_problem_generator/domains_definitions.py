#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 28 2020

@author: alvin
"""

import random
import copy


EQUALITY = 'eq'
INEQUALITY = 'neq'


class Object:
    def __init__(self, line = None, type_ = None, objects = None):                       # Example of line: waypoint: {wp0, wp1, wp2, wp3};
        if line:
            self.type = line[: line.find(':')].strip()
            objects = line[line.find('{')+1 : line.find('}')].split(',')
            self.objects = [o.strip() for o in objects if o.strip()]
        else:
            self.type = type_
            self.objects = objects

    def intersect(self, typed_objects):
        if typed_objects:
            if self.type == typed_objects.type:
                return Object(type_ = self.type, objects = [obj for obj in self.objects if obj in typed_objects.objects])
        return Object(type_ = self.type, objects = self.objects)

    def print(self):
        result = self.type + ':'
        for obj in self.objects:
            result += ' ' + obj
        return result

class Parameter:
    def __init__(self, type_name, position):
        self.type = type_name                       # e.g waypoint
        self.position = position                    # e.g an int that represents position of this parameter in the fluent, starts from 0
    
    def __eq__(self, other): 
        return self.type == other.type and self.position == other.position

class Probability:
    def __init__(self, min_range = 0.0, max_range = 1.0):
        self.min_range = min_range
        self.max_range = max_range
    
    def randomize(self):                            # return a random probability from 0 to 1.0 in increments of 0.1
        return random.randint(self.min_range*10, self.max_range*10)/10


class Fluent:
    def __init__(self, line):                       # Example of line: COMM_TOWER(wp3);
        self.name = None
        self.parameters = None
        self.value = None
        if '(' in line and ')' in line:
            self.name = line[: line.find('(')].strip()
            parameters = line[line.find('(')+1 : line.find(')')].split(',')
            self.parameters = [p.strip() for p in parameters]
            if '=' in line:                         # fluent has numeric value
                self.value = float(line[line.find('=')+1 : line.find(';')])
        self.substituted = []

    def copy(self):
        other = Fluent('')
        other.name = self.name
        other.parameters = self.parameters.copy()
        other.value = self.value
        other.substituted = self.substituted.copy()
        return other
        
    def __eq__(self, other):
        if self.name != other.name:
            return False
        if len(self.parameters) == len(other.parameters):
            for p1, p2 in zip(self.parameters, other.parameters):
                if not (p1 == p2):
                    return False
        else:
            return False
        if self.value is not None and other.value is not None:
            return self.value == other.value
        elif self.value is None and other.value is None:
            return True
        else:
            return False
        return True

    def substitute(self, obj, position):
        if position >= len(self.parameters):
            raise Exception('position cannot be >= number of parameters in fluent')
        if position not in self.substituted:                # can only substitute each parameter once (this is more for computational speed as fluent is randomized in a loop)
            self.parameters[position] = obj
            self.substituted.append(position)
            return True
        else:
            return False                                    # already substituted)

    def isProper(self):
        return self.name is not None

    def print(self):
        if not self.isProper():
            print("Null fluent")
            return ""
        output = self.name + '('
        first = True
        for p in self.parameters:
            if first:
                first = False
            else:    
                output += ', '
            output += p
        output += ')'
        if self.value is not None:
            output += ' = ' + str(self.value)
        return output


class RandomFluent:
    def __init__(self, name, parameters, value = None):     # string, list of Parameters, Probability
        self.name = name
        self.parameters = parameters
        self.value = value

    def getPosition(self, obj_type):
        for p in self.parameters:
            if p.type == obj_type:
                return p.position
        raise Exception('RandomFluent does not have a parameter with type ' + obj_type)

    # for each parameter, find the list of objects available and replace object in fluent with a random object
    def randomize(self, fluent, objects, mutex_fluents = [], mutex_objects = []):
        verbose = False
        attempt = 0
        while True:
            grounded_fluent = copy.deepcopy(fluent)
            bindings = []
            # randomly ground each parameter in fluent
            for p in self.parameters:
                for o in objects:
                    if o.type == p.type:
                        objects_ = [o for o in o.objects if o not in mutex_objects]
                        if not objects_:
                            raise Exception('No more valid objects to use after removing those that have been used for \'' + \
                                             fluent.name + '\' with parameter \'' + p.type + '\'')
                        obj = random.choice(objects_)
                        if (grounded_fluent.substitute(obj, p.position)):
                            bindings.append(Binding(obj, o.type))
                            if verbose:
                                print('RandomFluent::randomize: using binding ' + obj + ' for type ' + o.type + ' --> ' + grounded_fluent.print())
                        else:
                            # fluent already substituted, get its object at p.position
                            bindings.append(Binding(grounded_fluent.parameters[p.position], o.type))
                        break
            if self.value is not None:
                grounded_fluent.value = self.value.randomize()
            cont = False
            # if mutex_fluents is given, check if random fluent is in mutex_fluents
            for tfluent in mutex_fluents:
                if grounded_fluent == tfluent:
                    cont = True
                    if verbose:
                        print('    MUTEX  ' + tfluent.print() + ' is violated by ' + grounded_fluent.print())
                    break
                elif verbose:
                    print('    MUTEX  ' + tfluent.print() + ' is NOT violated by ' + grounded_fluent.print())
            if not cont:
                break
            attempt += 1
            if (attempt > 100):         # unable to randomize fluent, abort
                return None, None
        return grounded_fluent, bindings


class Binding:
    def __init__(self, obj, obj_type):
        self.obj = obj
        self.obj_type = obj_type
        
    def print(self):
        return self.obj_type + ' = ' + self.obj


class ConstrainedFluents:
    def __init__(self, fluents, constraint, typed_objects = None, unique_mapping = False):
        if len(fluents) != 2:
            raise Exception('Constraint must be between two fluents')
        self.fluents = fluents
        if constraint is not EQUALITY and constraint != INEQUALITY:
            raise Exception('Constraint must be either \'' + EQUALITY + '\' or \'' + INEQUALITY + '\'')
        self.constraint = constraint
        if typed_objects:
            self.typed_objects_to_use = Object(line = typed_objects)
        else:
            self.typed_objects_to_use = None
        # if unique_mapping is True, then the randomized binding for both constrained fluents must consider their own binding
        # Example: given {o1, o2, o3, o4, 05} objects, and randomized fluents f1(o1), f1(o2), f2(o3) --> remaining objects for f1 and f2 are {o4, o4}
        # if unique_mapping is False, then consider the binding of the other constrained fluent
        # Example: given {o1, o2, o3, o4, 05} objects, and randomized fluents f1(o1), f1(o2), f2(o3) --> remaining objects for f1 is {o1, o2, o4, o5} and f2 is {o3, o4, o5}
        self.unique_mapping = unique_mapping
        self.bindings = []

    def getNames(self):
        return [f.name for f in self.fluents]
    
    def reset(self):
        self.bindings = []

    # for each parameter, find the list of objects available and replace object in fluent with a random object
    # objects is a list of Object class
    def randomize(self, fluent, objects, mutex_fluents = [], mutex_objects = []):
        verbose = False
        cfluent = None
        cIndex = 0                                          # index of fluent in this list of constrained fluents
        for f in self.fluents:
            if f.name == fluent.name:
                cfluent = f
                break
            cIndex += 1
        if not cfluent:
            return None

        # this only works if there are 2 constrained fluents
        bindings_in_use = []
        if self.bindings:
            if self.unique_mapping:
                bindings_in_use = self.bindings[0] + self.bindings[1]
            elif cIndex == 0:
                bindings_in_use = self.bindings[1]          # get the bindings used by the other constrained fluent
            else:
                bindings_in_use = self.bindings[0]
            
        attempt = 0
        remaining_objects = None
        
        while True:
            grounded_fluent = copy.deepcopy(fluent)
            # apply binding if there is any
            if self.constraint == EQUALITY:
                for binding in bindings_in_use:
                    grounded_fluent.substitute(binding.obj, cfluent.getPosition(binding.obj_type))
            elif self.constraint == INEQUALITY:
                remaining_objects = copy.deepcopy(objects)
                # remove all objects that are not in typed_objects_to_use
                remaining_objects = [typed_objects.intersect(self.typed_objects_to_use) for typed_objects in remaining_objects]
                # remove objects which have been used in a binding from the set of all objects
                for binding in bindings_in_use:
                    for typed_objects in remaining_objects:
                        if typed_objects.type == binding.obj_type:
                            typed_objects.objects = [obj for obj in typed_objects.objects if obj != binding.obj]
                            if not typed_objects.objects:
                                raise Exception('Inequality Constraint between ' + \
                                                self.fluents[0].name + ' and ' + \
                                                self.fluents[1].name + \
                                                ' cannot be satisfied, not enough objects of type \'' + \
                                                binding.obj_type + '\' for ' +\
                                                self.fluents[cIndex].name)
                            # break
                if verbose:
                    print('Remaining objects for constrained fluent...')
                    for typed_objects in remaining_objects:
                        print(typed_objects.print())
                # inefficient but simple coding, now bind grounded_fluent with remaining objects
                # inefficient because the same parameter might be binded multiple times
                for binding in bindings_in_use:
                    for typed_objects in remaining_objects:
                        if typed_objects.type == binding.obj_type:
                            randomly_picked_remaining_obj = random.choice(typed_objects.objects)
                            grounded_fluent.substitute(randomly_picked_remaining_obj, cfluent.getPosition(binding.obj_type))
                            break
            else:
                raise NotImplementedError('Can only support equality or inequality constraint')
            if remaining_objects:
                grounded_fluent, bindings = cfluent.randomize(grounded_fluent, remaining_objects, mutex_fluents, mutex_objects)
            else:
                grounded_fluent, bindings = cfluent.randomize(grounded_fluent, objects, mutex_fluents, mutex_objects)
            if grounded_fluent is not None:
                if not self.bindings:
                    # construct a list of empty list, 1 list for each constrained fluent
                    self.bindings = [ [] for _ in range(len(self.fluents)) ]
                # bindings are added to the specific fluent, this is for INEQUALITY constraint to work
                self.bindings[cIndex] += bindings
                if verbose:
                    print('For constrained fluent: ' + grounded_fluent.print() + ' add bindings:')
                    for binding in bindings:
                        print('    ' + binding.print())
                return grounded_fluent
        attempt += 1
        if attempt > 100:
            return None


def has_common(list1, list2):
    for v1 in list1:
        for v2 in list2:
            if v1 == v2:
                return True
    return False


class Domain:
    def __init__(self, name, fluents = [], constrained_fluents = [], mutex_fluents_mapping = [], unique_fluents_mapping = [], second_randomization = False, warn_msg = ''):
        self.name = name                                                # name of domain
        self.fluents = fluents                                          # list of RandomFluents to be randomized in binding
        self.constrained_fluents = constrained_fluents                  # list of (tuples of RandomFluents for fluents to be randomized while obeying the constaint for their bindings)
        self.mutex_fluents_mapping = mutex_fluents_mapping              # list of pairs of fluents where [0] is the non-fluent name and [1] is the fluent name (e.g OBJECT_GOAL and object_at are pairs)
        self.unique_fluents_mapping = unique_fluents_mapping            # list of fluent names which must have unique parameter binding
        self.second_randomization = second_randomization                # if True, this domain with constraints is for 2nd round of randomization (handled by rpg.py); 
                                                                        # first, randomized using the original .rddl instance, then randomized again using the newly generated randomized .rddl instances
        self.warn_msg = warn_msg
        self.check()
        
    def check(self):
        rf_names = [fluent.name for fluent in self.fluents]
        for i in range(len(self.constrained_fluents)):
            if has_common(self.constrained_fluents[i].getNames(), rf_names):
                    raise NotImplementedError('Cannot support the same fluent in both ConstrainedFluents and RandomFluent --> remove fluent from RandomFluent instead')
            for cfluents in self.constrained_fluents:
                typed_parameter_to_be_randomized = None
                if cfluents.typed_objects_to_use:
                    typed_parameter_to_be_randomized = cfluents.typed_objects_to_use.type
                for fluent in cfluents.fluents:
                    if len(fluent.parameters) > 1:
                        raise NotImplementedError('Cannot support more than 1 parameter')
                    if len(fluent.parameters) == 1:
                        if typed_parameter_to_be_randomized is None:
                            typed_parameter_to_be_randomized = fluent.parameters[0].type
                        elif typed_parameter_to_be_randomized != fluent.parameters[0].type:
                            raise Exception('Parameter to be randomized has to be the same, these do not match: ' + typed_parameter_to_be_randomized + ' and ' + fluent.parameters[0].type)
            for j in range(i+1, len(self.constrained_fluents)):
                if has_common(self.constrained_fluents[i].getNames(), self.constrained_fluents[j].getNames()):
                    raise NotImplementedError('Cannot support RandomFluent constrained more than once')
        for fluent in self.fluents:
            if len(fluent.parameters) > 1:
                raise NotImplementedError('Cannot support more than 1 parameter')

    def randomizeFluent(self, fluent, objects, existing_fluents=[], mutex_fluents = []):     # mutex_fluents is list of Fluent class
        if fluent.name is None:
            return False
        substituted_mutex_fluents = self.getMutex(mutex_fluents)
        # if there are fluents randomized which need to be unique with current fluent that is being randomized
        # get their objects and remove it from list of possible objects that can be used to randomize current fluent
        objects_used = []
        if existing_fluents:
            # unique_fluent_names = [fluent.name for fluent in self.unique_fluents_mapping]
            for unique_fluent in self.unique_fluents_mapping:
                if fluent.name == unique_fluent.name:
                    # remove objects that have already been used from the list of objects that can be binded to random fluent
                    for parameter in unique_fluent.parameters:
                        for existing_fluent in existing_fluents:
                            if existing_fluent.name == fluent.name:
                                # get object for the parameter in the position of interest
                                objects_used.append(existing_fluent.parameters[parameter.position])
        # randomize constrained fluent
        for cf in self.constrained_fluents:
            if fluent.name in cf.getNames():
                return cf.randomize(fluent, objects, mutex_fluents=substituted_mutex_fluents, mutex_objects=objects_used)
        # find the random fluent to randomly ground
        for rf in self.fluents:
            if fluent.name == rf.name:
                return rf.randomize(fluent, objects, mutex_fluents=substituted_mutex_fluents, mutex_objects=objects_used)[0]
        return False
        
    def resetConstrainedFluents(self):
        for cf in self.constrained_fluents:
            cf.reset()

    # return a set of fluents that randomized fluents cannot be equal to
    # this generates initial states that do not match the goal state
    def getMutex(self, mutex_fluents):
        substituted_mutex_fluents = []
        for tf in mutex_fluents:
            fluent = copy.deepcopy(tf)
            for f1, f2 in self.mutex_fluents_mapping:
                if fluent.name == f1:
                    fluent.name = f2                                            # substitute fluent name (e.g change OBJECT_GOAL to object_at)
                    substituted_mutex_fluents.append(fluent)
                elif fluent.name == f2:
                    fluent.name = f1                                            # substitute fluent 
                    substituted_mutex_fluents.append(fluent)
        return substituted_mutex_fluents

    def printWarning(self):
        if warn_msg:
            print('******************\n    WARNING\n******************\n'+warn_msg)


class Domains:
    def __init__(self):
        self.domains = []
    
    def add(self, domain):
        for d in self.domains:
            if d.name == domain.name and d.second_randomization == domain.second_randomization:
                raise Exception('Domain "' + domain.name + '"" already exists')
        self.domains.append(domain)

    def hasDoubleRandomization(self, name):
        for domain in self.domains:
            if name == domain.name:
                if domain.second_randomization:
                    return True
        return False

    def getDomain(self, name, second_randomization = False):
        for domain in self.domains:
            # there may be two domains with the same domain_name but one of them is for 2nd round of randomization
            if name == domain.name and second_randomization == domain.second_randomization:
                return domain
        if second_randomization:
            raise Exception('No such domain "' + name + '"" with second randomization specified in domains_definitions.py!')
        else:
            raise Exception('No such domain "' + name + '"" specified in domains_definitions.py!')
        return None



#########################################
### Define how domains are randomized ###
#########################################
lsof_domains = Domains()

################## turtlebot_survey ##################
# add the fluents to be randomized, specify the parameter/s (list of parameters) which will be randomized (its type and position starting from 0)
rfluents = [
    RandomFluent('COMM_TOWER', [Parameter('waypoint', 0)]),                # argument 0-th of type 'waypoint' of fluent 'COMM_TOWER' shall be randomized
    RandomFluent('OBJECT_AT', [Parameter('waypoint', 1)])
]
# add fluents to be randomized with the same object (e.g robot initial position must be where dock is at if docked is true)
cfluents = [
    ConstrainedFluents([ RandomFluent('DOCK_AT', [Parameter('waypoint', 0)]), RandomFluent('robot_at', [Parameter('waypoint', 1)]) ], EQUALITY)
]
lsof_domains.add(Domain(name='turtlebot_survey', fluents=rfluents, constrained_fluents=cfluents))


################## turtlebot & turtlebot_goal ##################
cfluents = [
    ConstrainedFluents([ RandomFluent('DOCK_AT', [Parameter('waypoint', 0)]), RandomFluent('robot_at', [Parameter('waypoint', 1)]) ], EQUALITY)
]
lsof_domains.add(Domain(name='turtlebot', constrained_fluents=cfluents))
lsof_domains.add(Domain(name='turtlebot_goal', constrained_fluents=cfluents))


################## tiago_fetch ##################
rfluents = [
    RandomFluent('OBJECT_GOAL', [Parameter('waypoint', 1)]),
    RandomFluent('object_at', [Parameter('waypoint', 1)]),
    RandomFluent('robot_at', [Parameter('waypoint', 1)]),
    RandomFluent('PROB_DROP_OBJ', [], Probability(0.0, 1.0)),                 # fluent with randomized probability
    RandomFluent('PROB_POOR_GRASP', [], Probability(0.0, 0.5)),
    RandomFluent('PROB_LOSING_LOCALISATION', [], Probability(0.0, 0.1))]
unique_fluents_mapping = [
    RandomFluent('OBJECT_GOAL', [Parameter('waypoint', 1)]),                  # all randomized OBJECT_GOAL must have different waypoint
    RandomFluent('object_at', [Parameter('waypoint', 1)])                     # all randomized object_at must have different waypoint
]
mutex_fluents_mapping = [('OBJECT_GOAL', 'object_at')]                        # parameters of OBJECT_GOAL cannot have the exact same parameters as any object_at
# unique_fluents_mapping & mutex_fluents_mapping prevents these two fluents from being equal    
lsof_domains.add(Domain(name='tiago_fetch', fluents=rfluents, mutex_fluents_mapping=[('OBJECT_GOAL', 'object_at')], unique_fluents_mapping=unique_fluents_mapping))


################## husky_inspection ##################
rfluents = [
    RandomFluent('POI_AT', [Parameter('waypoint', 1)]),
    RandomFluent('BASE', [Parameter('waypoint', 0)]),
    RandomFluent('robot_at', [Parameter('waypoint', 1)])
]
lsof_domains.add(Domain(name='husky_inspection', fluents=rfluents))


################## recon2 ##################
# DEPRECATED --> this allows OBJECT_AT and HAZARD to be at same location
# rfluents = [
#     RandomFluent('OBJECT_AT', [Parameter('pos', 1)]),
#     RandomFluent('HAZARD', [Parameter('pos', 0)])
# ]
# cfluents = [
#     ConstrainedFluents([ RandomFluent('BASE', [Parameter('pos', 0)]), RandomFluent('agentAt', [Parameter('pos', 1)]) ], EQUALITY),
# ]
# unique_fluents_mapping = [
#     RandomFluent('OBJECT_AT', [Parameter('pos', 1)])                         # all randomized OBJECT_AT must have different waypoint
# ]
# mutex_fluents_mapping = [('BASE', 'HAZARD')]
# lsof_domains.add(Domain(name='recon2', fluents=rfluents, constrained_fluents=cfluents, mutex_fluents_mapping=mutex_fluents_mapping, unique_fluents_mapping=unique_fluents_mapping))


################## recon2 ##################
cfluents = [
    ConstrainedFluents([ RandomFluent('BASE', [Parameter('pos', 0)]), RandomFluent('agentAt', [Parameter('pos', 1)]) ], EQUALITY),
    ConstrainedFluents([ RandomFluent('HAZARD', [Parameter('pos', 0)]), RandomFluent('OBJECT_AT', [Parameter('pos', 1)]) ], INEQUALITY)     # value of HAZARD cannot be used for OBJECT_AT and vice versa, no constraint between OBJECT_AT
]
unique_fluents_mapping = [
    RandomFluent('OBJECT_AT', [Parameter('pos', 1)])                         # all randomized OBJECT_AT must have different waypoint
]
mutex_fluents_mapping = [('BASE', 'HAZARD')]
lsof_domains.add(Domain(name='recon2', constrained_fluents=cfluents, mutex_fluents_mapping=mutex_fluents_mapping, unique_fluents_mapping=unique_fluents_mapping))


################## robot_inspection ##################
# DEPRECATED --> this allows OBJECT_AT to be at the same location, and randomize location of COMM_TOWER
# rfluents = [
#     RandomFluent('OBJECT_AT', [Parameter('pos', 1)]),
#     RandomFluent('COMM_TOWER', [Parameter('pos', 0)])]
# lsof_domains.add(Domain(name='robot_inspection', fluents=rfluents))


################## robot_inspection ##################
rfluents = [
    RandomFluent('OBJECT_AT', [Parameter('pos', 1)])
]
unique_fluents_mapping = [
    RandomFluent('OBJECT_AT', [Parameter('pos', 1)])                        # all randomized OBJECT_AT must have different waypoint
]
lsof_domains.add(Domain(name='robot_inspection', fluents=rfluents, unique_fluents_mapping=unique_fluents_mapping))


################## taxi ##################
# for Original Taxi domain, can't randomize Taxi domain, too many constraints (how to make passenger_at EQUAL TAXI_STAND, and DESTINATION EQUAL TAXI_STAND?)
# instead, in practice, we don't need TAXI_STAND, just a DESTINATION per passenger
rfluents = [
    RandomFluent('taxi_at', [Parameter('pos', 1)])
]

# value of passenger_at cannot be used for DESTINATION and vice versa and is limited to a set of pos values (the 4 corners of the grid)
# to generate RPG for each instance, remove other .rddl instance files from /domains/robots/
cfluents = [
    # ConstrainedFluents([ RandomFluent('passenger_at', [Parameter('pos', 1)]), RandomFluent('DESTINATION', [Parameter('pos', 1)]) ], INEQUALITY, 'pos: {wp1, wp3, wp7, wp9}'),     # for sq3
    # ConstrainedFluents([ RandomFluent('passenger_at', [Parameter('pos', 1)]), RandomFluent('DESTINATION', [Parameter('pos', 1)]) ], INEQUALITY, typed_objects = 'pos: {wp1, wp4, wp13, wp16}'),     # for sq4
    ConstrainedFluents([ RandomFluent('passenger_at', [Parameter('pos', 1)]), RandomFluent('DESTINATION', [Parameter('pos', 1)]) ], INEQUALITY, 'pos: {wp1, wp5, wp21, wp25}'),   # for sq5
]
# unique_fluents_mapping = [
#     RandomFluent('passenger_at', [Parameter('pos', 1)])                     # all randomized passenger_at must have different position
#     RandomFluent('DESTINATION', [Parameter('pos', 1)]),                     # all randomized DESTINATION must have different position
# ]
warn_msg = 'taxi instances must be randomized one at a time with different ConstrainedFluents for each instance'
lsof_domains.add(Domain(name='taxi', fluents=rfluents, constrained_fluents=cfluents, warn_msg = warn_msg))


################## tiago_hri ##################
# this domain needs to be randomized twice because we can't use the same state fluent twice in ConstrainedFluents
# 1st round of randomization: randomize objects for PERSON_GOAL_OBJECT_WITH and PERSON_GOAL_OBJECT_AT and each object is only used once
cfluents = [
    ConstrainedFluents([ RandomFluent('PERSON_GOAL_OBJECT_WITH', [Parameter('obj', 1)]), RandomFluent('PERSON_GOAL_OBJECT_AT', [Parameter('obj', 1)]) ], INEQUALITY, unique_mapping = True),
]
unique_fluents_mapping = [
    RandomFluent('PERSON_GOAL_OBJECT_AT', [Parameter('obj', 1)]),                       # all randomized PERSON_GOAL_OBJECT_AT must have different objects
    RandomFluent('PERSON_GOAL_OBJECT_WITH', [Parameter('obj', 1)])                      # all randomized PERSON_GOAL_OBJECT_WITH must have different objects
]
lsof_domains.add(Domain(name='tiago_hri', fluents=rfluents, constrained_fluents=cfluents))

# 2nd round of randomization: randomize waypoints for object_at and PERSON_GOAL_OBJECT_AT which cannot be equal
cfluents = [
    # it is ok to specify extraneous waypoints that an instance does not have, only waypoints in a .rddl instance will be used
    ConstrainedFluents([ RandomFluent('object_at', [Parameter('waypoint', 1)]), RandomFluent('PERSON_GOAL_OBJECT_AT', [Parameter('waypoint', 2)]) ], INEQUALITY, 'waypoint: {wp1, wp2, wp3, wp5, wp6, wp7}'),
]
lsof_domains.add(Domain(name='tiago_hri', fluents=rfluents, constrained_fluents=cfluents, second_randomization=True))


################## blocksworld ##################
# this domain is not randomised, just use this to generate the files and manually randomise it
lsof_domains.add(Domain(name='blocksworld'))