#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 28 2020

@author: alvin
"""

import os
import glob
import sys
import copy
import random

try:
    import random_problem_generator.domains_definitions as dd   # when rpg.py is imported
except:
    import domains_definitions as dd                            # when rpg.py is called as main

keywords_order = ['nfs', 'nf', 'd', 'o', 'i', 'init']           # always iterate keywords using this order, do not use keywords.items() which does not have a fixed order
keywords = {'nfs': 'non-fluents {', 'nf': 'non-fluents ', 'd': 'domain', 'o': 'objects', 'i': 'instance', 'init': 'init-state'}
# TAB = '\t'
TAB = ' '

# -----------------------------
# -----------------------------
# -----------------------------
#       RUN COMMANDS
# -----------------------------
# -----------------------------
# -----------------------------

def readInstanceFile(filename, randomize_non_fluents):
    def find_keyword(line):
        for key in keywords_order:
            if keywords[key] in line:
                return key
        return None

    source = open(filename, 'r')
    domain_name = None
    instance_name = None
    template = []
    objects = []
    non_fluents = []
    randomize_lines = []
    instance_name_lines = []
    prev_section = None
    line_num = 1

    for line in source:
        section = find_keyword(line)
        # print(section)
        if section is None:
            section = prev_section
        if section == 'nf' and section != 'nfs':
            section = prev_section
            instance_name_lines.append(line_num)
        if section == 'i':
            instance_name_lines.append(line_num)
            instance_name = line[line.find(keywords['i'])+len(keywords['i']) : line.find('{')].strip()

        # if section is None:
        #     section = 'Nil'
        # print(section + ' - ' + line)

        if section == 'nfs':
            if randomize_non_fluents:
                # change non-fluents
                randomize_lines.append((section, line_num))
            else:
                fluent = dd.Fluent(line)
                if fluent.isProper():
                    non_fluents.append(fluent)
        elif section == 'd' and keywords['d'] in line:
            # get domain name
            domain_name = line[line.find('=')+1 : line.find('_mdp')].strip()
        elif section == 'o':
            # read & store what objects are used
            objects.append(dd.Object(line=line))
        elif section == 'init':
            # change init-state
            randomize_lines.append((section, line_num))

        prev_section = section
        template.append(line)
        line_num += 1

    source.close()
    objects = [o for o in objects if o.objects]
    return (domain_name, instance_name, objects, non_fluents, template, randomize_lines, instance_name_lines)


def generateRandomInstance(filename, domain_name, template, objects, non_fluents, randomize_lines, instance_name_lines, count = None, second_randomization = False):
    try:
        domain = dd.lsof_domains.getDomain(domain_name, second_randomization)
    except:
        return False                                # instance file is not defined in domains_definitions.py
    if count == 0:
        domain.printWarning()
    destination = open(filename, 'w')               # temp file
    instance_name = None
    non_fluents_for_inst = []                       # cannot append to non_fluents as lists are passed in as reference and this will affect the next iteration of random instance
    randomized_fluents_for_inst = []                # this is for domains where fluents cannot be repeated (e.g more than one object at a location)
    line_num = 1
    random.seed(count)
    
    # read each line of .rddl file and re-write it if required
    for line in template:
        if line_num in instance_name_lines:
            if instance_name is None:
                if count is None:
                    instance_name = line[line.find(keywords['nf'])+len(keywords['nf']) : line.find('{')].strip()
                else:
                    instance_name = line[line.find(keywords['nf'])+len(keywords['nf']) : line.find('{')].strip() + '_' + str(count)
            if '{' in line:
                if count is None:
                    line = line[: line.find('{')-1] + ' {\n'
                else:
                    line = line[: line.find('{')-1] + '_' + str(count) + ' {\n'
            else:
                line = line[: line.find('=')+1] + ' ' + instance_name + ';\n'
        else:
            for section, rline in randomize_lines:  # randomize_lines is a list (section, line num)
                if line_num == rline:               # this line in .rddl is to be randomized
                    # print(section)
                    # change non-fluents or change init-state
#                    if section == 'nfs':
#                        fluent = domain.randomizeFluent( \
#                                                         dd.Fluent(line), \
#                                                         objects, \
#                                                         existing_fluents=randomized_fluents_for_inst)
#                        if fluent:
#                            non_fluents_for_inst.append(fluent)       # prevent randomization of initial state to match randomized goal state
#                    else:
#                        fluent = domain.randomizeFluent( \
#                                                         dd.Fluent(line), \
#                                                         objects, \
#                                                         existing_fluents=randomized_fluents_for_inst, \
#                                                         tabu_fluents=non_fluents+non_fluents_for_inst)

                    # print(line)
                    fluent = domain.randomizeFluent( \
                                                     dd.Fluent(line), \
                                                     objects, \
                                                     existing_fluents=randomized_fluents_for_inst, \
                                                     mutex_fluents=non_fluents+non_fluents_for_inst)
                    # if isinstance(fluent, dd.Fluent):
                    #    print('Randomized: ' + fluent.print())
                    if section == 'nfs' and fluent:
                        non_fluents_for_inst.append(fluent)       # prevent randomization of initial state to match randomized goal state
                    if fluent:
                        randomized_fluents_for_inst.append(copy.deepcopy(fluent))
                        num_leading_space = len(line) - len(line.lstrip())
                        line = num_leading_space*TAB + fluent.print() + ';\n'
                    elif fluent is None:
                        raise Exception('Unable to randomize fluent in :' + line)
        line_num += 1
        destination.write(line)

    # close files and overwrite original .cfg file
    destination.close()
    domain.resetConstrainedFluents()
    return True


# original_instances is a list of instances names that are not randomly generated
# if this is given, then for each original instance, return a list of it's randomly generated instances (i.e return a list of list)
# if not given, just return list of randomly generated instances names
def getInstances(folder, original_instances = None):
    instances = glob.glob(folder+'/*.rddl')         # list of file paths with matching .rddl
    rpg_instances = []
    for i in original_instances:
        rpg_instances.append([])
    for instance in instances:
        (domain_name, instance_name, objects, non_fluents, template, randomize_lines, instance_name_lines) = readInstanceFile(instance, False)
        if original_instances:
            try:
                original_instance_name = instance_name[: instance_name.rfind('_')]                                       # Example of original_instance_name: turtlebot_survey_inst_mdp__p1
                # index = original_instances.index(original_instance_name)                                               # Find index in the list 'original_instances' which contain the entry == original_instance_name
                indices = [i for i, orig_inst in enumerate(original_instances) if orig_inst == original_instance_name]   # this is better, able to deal with duplicated entries in original_instances
                for index in indices:
                    rpg_instances[index].append(instance_name)
            except ValueError:
                continue    # instance is not in instances
    return rpg_instances


def run(filename, num_random_inst, randomize_non_fluents, desired_domain_names = None, dest_folder = None, second_randomization = False):
    (domain_name, instance_name, objects, non_fluents, template, randomize_lines, instance_name_lines) = readInstanceFile(filename, randomize_non_fluents)
    if not isinstance(desired_domain_names, list):
        desired_domain_names = [desired_domain_names]
    if not domain_name or not instance_name:
        return                                                                  # instance file cannot be parsed
    elif desired_domain_names and domain_name not in desired_domain_names:
        return

    perform_double_randomization = dd.lsof_domains.hasDoubleRandomization(domain_name) and not second_randomization # domain needs double randomization and this is first round of randomization
    if perform_double_randomization:
        generated_files = []
        # store files in another folder
        if dest_folder:
            dest_folder1 = dest_folder.rstrip('/')
            dest_folder1 += '/first_rpg/'
        else:
            dest_folder1 = filename[: filename.rfind('/')] + '/first_rpg/'
        if not os.path.exists(dest_folder1):
            os.makedirs(dest_folder1, exist_ok=True)
        for count in range(num_random_inst):
            dest_filename = dest_folder1 + '/' + instance_name + '_' + str(count) + '.rddl'
            if not generateRandomInstance(dest_filename, domain_name, template, objects, non_fluents, randomize_lines, instance_name_lines, count):
                break                                                           # instance file is not defined in domains_definitions.py
            generated_files.append(dest_filename)
        print('First round of randomization: generated ' + str(len(generated_files)) + ' random instances for domain: ' + domain_name + ' and instance: ' + instance_name)
        instances = glob.glob(dest_folder1+'/*.rddl')                           # get all files with extension .rddl (these are the newly randomly generated files) 
        # now perform secound round of randomization, generate only 1 RPG for each RPG of the first round of randomization
        for instance in instances:
            generated_files = run(instance, 1, randomize_non_fluents, desired_domain_names = domains, dest_folder = dest_folder, second_randomization = True)
    else:
        if dest_folder:
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder, exist_ok=True)
        generated_files = []
        for count in range(num_random_inst):
            if second_randomization:
                count = None                                                        # do not append _# for second round of randomization as it is already done in first round
            if dest_folder:
                # instance_name = filename[filename.rfind('/') :]
                # dest_filename =  dest_folder + instance_name[: instance_name.find('.')] + '_' + str(count) + instance_name[instance_name.find('.') :]
                if count is None:
                    dest_filename = dest_folder + '/' + instance_name + '.rddl'
                else:
                    dest_filename = dest_folder + '/' + instance_name + '_' + str(count) + '.rddl'
            else:
                if count is None:
                    dest_filename = filename[: filename.find('.')] + filename[filename.find('.') :]
                else:
                    dest_filename = filename[: filename.find('.')] + '_' + str(count) + filename[filename.find('.') :]
            if not generateRandomInstance(dest_filename, domain_name, template, objects, non_fluents, randomize_lines, instance_name_lines, count = count, second_randomization = second_randomization):
                break                                                               # instance file is not defined in domains_definitions.py
            generated_files.append(dest_filename)
        if second_randomization:
            print('Second round of randomization: generated ' + str(len(generated_files)) + ' random instances for domain: ' + domain_name + ' and instance: ' + instance_name)
        else:
            print('Generated ' + str(len(generated_files)) + ' random instances for domain: ' + domain_name + ' and instance: ' + instance_name)
        return generated_files


def help():
    return './rpg.py [instance filename or folder containing instances] [num of instances to generate] <randomize_non_fluents = True or False> <dest folder = folder of instance>\n \
            Example:\n \
                 ./rpg.py /media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/domains/robots 30 True /media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/domains/robots_rpg2/'



if __name__ == "__main__":
    # domains = ['turtlebot_survey', 'tiago_fetch', 'taxi', 'robot_inspection', 'recon2', 'husky_inspection', 'tiago_hri']
    domains = ['blocksworld']
    
    if len(sys.argv) < 3:
        raise Exception(help())
    else:
        if '.rddl' in sys.argv[1]:
            instances = [sys.argv[1]]
            folder = None
        else:
            folder = sys.argv[1]
        
        if len(sys.argv) > 3:
            if sys.argv[3].lower() == 'true':
                randomize_non_fluents = True
            elif sys.argv[3].lower() == 'false':
                randomize_non_fluents = False
            else:
                raise Exception(help())
        else:
            randomize_non_fluents = True
        
        if len(sys.argv) > 4:
            dest_folder = sys.argv[4]                   # folder where RPG will be at
        else:
            dest_folder = None
        num_random_inst = int(sys.argv[2])
    
    if folder:
        instances = glob.glob(folder+'/*.rddl')         # get all files with extension .rddl
    
    for instance in instances:
        generated_files = run(instance, num_random_inst, randomize_non_fluents, desired_domain_names = domains, dest_folder = dest_folder)