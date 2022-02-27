#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:53:26 2019

@author: alvin

Compare the difference between feature sets
"""

import sys

PHRASE = 'features: '

def parse_file(logfile, verbose = False):
    try:
        if verbose > 1:
            print("Parsing file " + logfile)
        file = open(logfile, "r")
    except IOError:
        if verbose > 0:
            print(logfile + " does not exist")
        return False
    LFA_name = None
    features_map = {}
    line_num = 0
    for line in file:
        if ';' in line:
            delimiter = ');'
        else:
            delimiter = ')'
        line_num += 1
        if not line or line is "\n":
            continue
        if PHRASE in line and LFA_name:
            action = line[:line.find(' with ')]
            fluents = line[line.find(PHRASE)+len(PHRASE):]
            fluents = [f.strip()+')' for f in fluents.split(delimiter) if f.strip()]
            if LFA_name in features_map:
                features_map[LFA_name][action] = fluents
            else:
                features_map[LFA_name] = {action: fluents}
        else:
            LFA_name = line.strip()
    if '.' in logfile:
        results_file = logfile[:logfile.find('.')] + '_comparison' + logfile[logfile.find('.'):]
    else:
        results_file = logfile+'_comparison'
    print('Writing comparison to ' + results_file)
    f = open(results_file, "w")
    DONE = []
    for name1, action_features1 in features_map.items():
        for name2, action_features2 in features_map.items():
            if name1 == name2 or (name2, name1) in DONE:
                continue
            DONE.append((name1, name2))
            f.write('\n----------------------------------------------')
            f.write('\nFeatures in \'' + name1 + '\' but not in \'' + name2 + '\':')
            for action, features1 in action_features1.items():
                if action not in action_features2:
                    continue
                f.write('\n     ' + action + ':')
                at_least_once = False
                for f1 in features1:
                    if f1 not in action_features2[action]:
                        at_least_once = True
                        f.write(' ' + f1)
                if not at_least_once:
                    f.write(' none')
            f.write('\n-----------------------')
            f.write('\nFeatures in \'' + name2 + '\' but not in \'' + name1 + '\':')
            for action, features2 in action_features2.items():
                if action not in action_features1:
                    continue
                f.write('\n     ' + action + ':')
                at_least_once = False
                for f2 in features2:
                    if f2 not in action_features1[action]:
                        at_least_once = True
                        f.write(' ' + f2)
                if not at_least_once:
                    f.write(' none')
    f.close()



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Need 1 argument which specifies the filename of textfile containing features for each action fluent")
    else:
        parse_file(sys.argv[1])