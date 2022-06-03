#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:46:20 2019

@author: alvin
"""

import os
import experiments_utils as exp_utils

instance_prefix = 'inst_mdp'


class Domain:
    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise Exception('Domain must have name defined')
        if 'folder' not in kwargs:
            raise Exception('Domain must have folder defined')
        self.attributes = kwargs
    
    def getAttribute(self, attribute):
        return self.attributes.get(attribute, None)

    def getInstances(self, instance_indices):
        # instances = [name+'_inst'+i for i in instance_indices]
        instances = []
        for i in instance_indices:
            instances.append(self.attributes['name'] + '_' + instance_prefix + '__' + str(i))
        return instances

class Domains:
    def __init__(self):
        self.domains = []
    
    def add(self, domain):
        self.domains.append(domain)
    
    def getDomain(self, name, attribute = None):
        for domain in self.domains:
            if name == domain.getAttribute('name'):
                if attribute:
                    return domain.getAttribute(attribute)
                else:
                    return domain
        raise Exception('No such domain "' + str(name) + '"" specified in domains_utils.py!')
        return None

    # problem_instances is either a list [(domain, problem_instance)] or [domain]
    # if concatenate is true, return [(domain, [instance_1, instance_2, ..., instance_num])]
    # else return [(domain, instance_1), (domain, instance_2), ..., (domain, instance_num)]
    def getProblemInstances(self, problem_instances, num_instances, num_repetitions, starting_seed, concatenate):
        if num_instances == 0:
            raise Exception('num_instances must be > 0')
        if not isinstance(problem_instances, list):
            problem_instances = [problem_instances]
        problems = []
        for domain, instance in problem_instances:
            if self.getDomain(domain, 'rpg_folder'):
                if concatenate:
                    instances = []
                    for i in range(num_instances):
                        instances += [str(instance)+'_'+str(i+starting_seed-1)]
                    problems += [(domain, instances)]*num_repetitions
                else:
                    for i in range(num_instances):
                        problems += [(domain, str(instance)+'_'+str(i+starting_seed-1))]
            else:
                if concatenate:
                    problems += [(domain, [instance]*num_instances)]*num_repetitions
                else:
                    problems += [(domain, instance)]*num_instances*num_repetitions
        return problems
    
    # copies any file that has identifier in its filename, this can copy extraneous files (e.g., identifier or domain name is 'tiago', this will also copy 'tiago_fetch')
    def fileIsForDomain(self, filename, identifier, instance = ''):
        if isinstance(instance, list):
            return any([self.fileIsForDomain(filename, identifier, inst) for inst in instance])
        elif filename.find(identifier) != -1:
            if filename.find('inst') == -1 or filename.find('template') != -1:
                return True       # copy all files that are not instances files
            elif filename.find(instance) !=- 1:
                return True       # copy all instance files of it matches the requested instance
        return False

    def load(self, folder, problems = None, load_rpg = False):
        if not os.path.isdir(folder):
            os.makedirs(folder, exist_ok=True)
        else:
            exp_utils.remove_all_files_in_folder(folder, True)
        if problems is None:
            problems = []
            for domain in self.domains:
                problems.append(domain.getAttribute('name'))
        for problem in problems:
            if isinstance(problem, tuple):
                domain = problem[0]
                if isinstance(problem[1], list):
                    instances = [str(instance) for instance in problem[1]]
                else:
                    instances = str(problem[1])
                instances_given = True
            else:
                domain = problem
                instances = ['']
                instances_given = False
            source_folder = self.getDomain(domain, 'folder')
            files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f) )]
            name = self.getDomain(domain, 'name')
            target_files = [f for f in files if self.fileIsForDomain(f, name, instances)]
            rddl_files = [f for f in target_files if '.rddl' in f and 'inst' in f]
            pddl_files = [f for f in target_files if '.pddl' in f or '.ppddl' in f]
            # if not rddl_files:
            #     print('WARNING: \'' + name + '\' does not have .rddl files in its folder, check that filenames are prefixed with \'' + name + '_\'')
            # if not pddl_files:
            #     print('WARNING: \'' + name + '\' does not have .pddl files in its folder, check that filenames are prefixed with \'' + name + '_\'')
            exp_utils.copy_files(target_files, source_folder, folder)
            
            if not load_rpg:
                load_rpg = instances_given and not rddl_files    # specified instance might be an RPG instance, hence, can't find in folder, must find it in rpg_folder
            source_folder = self.getDomain(domain, 'rpg_folder')
            if load_rpg and source_folder:
                files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f) )]
                name = self.getDomain(domain, 'name')
                target_files = [f for f in files if self.fileIsForDomain(f, name, instances)]
                exp_utils.copy_files(target_files, source_folder, folder)



lsof_domains = Domains()
lsof_domains.add(Domain(
                    **{'name': 'blocksworld',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_rpg'),
                       'approx': None,
                       'empty': None}))
lsof_domains.add(Domain(
                    **{'name': 'tiago_hri',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_hri_mdp_approx.rddl'),
                       'latent': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_hri_mdp_latent.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'taxi',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg')}))
lsof_domains.add(Domain(
                    **{'name': 'grid_survey',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots')}))
lsof_domains.add(Domain(
                    **{'name': 'robot_inspection',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'deterministic': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'robot_inspection_mdp_deterministic.rddl'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'robot_inspection_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'robot_inspection_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'recon2',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'deterministic': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'recon2_mdp_deterministic.rddl'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'recon2_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'recon2_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'orca_inspection',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'orca', 'generated'),
                       'deterministic': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'orca_inspection_mdp_deterministic.rddl'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'orca_inspection_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'orca_inspection_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'husky_inspection',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'deterministic': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'husky_inspection_mdp_deterministic.rddl'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'husky_inspection_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'husky_inspection_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'turtlebot',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'turtlebot_goal',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_goal_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_goal_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'turtlebot_survey',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'deterministic': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_survey_mdp_deterministic.rddl'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_survey_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'turtlebot_survey_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'tiago',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'tiago_fetch',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots'),
                       'rpg_folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_rpg'),
                       'approx': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_fetch_mdp_approx.rddl'),
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'robots_incomplete', 'tiago_fetch_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'triangle_tireworld',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'triangle_tireworld_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'crossing_traffic',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'crossing_traffic_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'elevators',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'elevators_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'game_of_life',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'game_of_life_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'navigation',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'navigation_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'academic_advising',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'academic_advising_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'wildfire',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'wildfire_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'recon',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'recon_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'skill_teaching',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'skill_teaching_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'tamarisk',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'tamarisk_mdp_empty.rddl')}))
lsof_domains.add(Domain(
                    **{'name': 'sysadmin',
                       'folder': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc'),
                       'rpg_folder': None,
                       'approx': None,
                       'empty': os.path.join(exp_utils.mbrrl_path, 'domains', 'ippc_incomplete', 'sysadmin_mdp_empty.rddl')}))