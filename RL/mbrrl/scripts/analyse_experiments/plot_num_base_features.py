#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Uncomment the lines in FeatureSelectionAll.cpp and FeatureSelectionCPF.cpp to print the number of base features.
Run the experiments with MBFS and MFFS for small and large scale problems.

For MFFS:
    Open a terminal at the directory of the folder which contains all logfiles.

    Run this command:
        $ grep -r "Num of first order base features" > ../output.txt
        $ grep -r "Num of base features" > ../output.txt
    To get the number of base features. Copy and paste into the variable 'mffs_num_base_features' below. Just replicate the numbers 10 times since the number of base features do not change.

For MBFS:
    The results will be logged in analysis_cpf_features.log. Copy and paste into the variable 'mbfs_num_base_features' below.

@author: alvin
"""

import matplotlib.pyplot as plt
import math


domain_order = ['academic_advising', 'recon', 'triangle_tireworld', 'tiago_fetch', 'turtlebot_survey', 'tiago_hri']
domain_name = ['Academic Advising', 'Recon', 'Triangle Tireworld', 'Robot Fetch', 'Robot Inspection', 'Service Robot']
mbfs_num_base_features = {
    'recon2__3__GND': [199, 476, 1027, 1097, 1107, 1112, 1112, 1112, 1112, 1112],
    'recon2__3__FO': [33, 42, 69, 73, 73, 74, 74, 74, 74, 74],
    'recon2__6__GND': [401, 959, 1760, 1862, 1872, 1877, 1877, 1877, 1877, 1877],
    'recon2__6__FO': [33, 42, 69, 73, 73, 74, 74, 74, 74, 74],
    'academic_advising__3__GND': [83, 129, 155, 163, 163, 163, 163, 163, 163, 163],
    'academic_advising__3__FO': [9, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    'academic_advising__5__GND': [113, 179, 257, 297, 303, 303, 303, 303, 303, 303],
    'academic_advising__5__FO': [9, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    'triangle_tireworld__3__GND': [352, 3781, 7534, 7744, 7744, 7744, 7744, 7744, 7744, 7744],
    'triangle_tireworld__3__FO': [16, 22, 27, 33, 33, 33, 33, 33, 33, 33],
    'triangle_tireworld__6__GND': [1024, 23080, 46456, 47212, 47212, 47212, 47212, 47212, 47212, 47212],
    'triangle_tireworld__6__FO': [16, 22, 27, 33, 33, 33, 33, 33, 33, 33],
    'turtlebot_survey__de2__GND': [195, 408, 492, 507, 519, 523, 523, 537, 540, 540],
    'turtlebot_survey__de2__FO': [58, 83, 118, 126, 132, 134, 136, 136, 136, 136],
    'turtlebot_survey__de4__GND': [478, 1222, 1506, 1570, 1593, 1600, 1600, 1676, 1692, 1692],
    'turtlebot_survey__de4__FO': [57, 82, 117, 126, 132, 134, 136, 136, 136, 136],
    'tiago_fetch__d1__GND': [239, 624, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006],
    'tiago_fetch__d1__FO': [24, 37, 53, 54, 54, 54, 54, 54, 54, 54],
    'tiago_fetch__d2__GND': [1095, 4415, 10968, 10968, 10968, 10968, 10968, 10968, 10968, 10968],
    'tiago_fetch__d2__FO': [24, 37, 53, 54, 54, 54, 54, 54, 54, 54],
    'tiago_hri__1__GND': [310, 1012, 2060, 2096, 2096, 2096, 2096, 2096, 2096, 2096],
    'tiago_hri__1__FO': [44, 61, 112, 118, 118, 118, 118, 118, 118, 118],
    # 'tiago_hri__2__GND': [1770, 11474, 31488, 31860, 31860, 31860, 31860, 31860, 31860, 31860],
    # 'tiago_hri__2__FO': [44, 63, 125, 133, 133, 133, 133, 133, 133, 133],
    'tiago_hri__3__GND': [1770, 11474, 31488, 31860, 31860, 31860, 31860, 31860, 31860, 31860],
    'tiago_hri__3__FO': [44, 63, 125, 133, 133, 133, 133, 133, 133, 133],   
}

mffs_num_base_features = {
    'academic_advising__3__GND': [480, 480, 480, 480, 480, 480, 480, 480, 480, 480],
    'academic_advising__3__FO': [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
    'academic_advising__5__GND': [840, 840, 840, 840, 840, 840, 840, 840, 840, 840],
    'academic_advising__5__FO': [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
    'tiago_hri__3__FO': [162, 162, 162, 162, 162, 162, 162, 162, 162, 162],
    'recon2__3__GND': [1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176, 1176],
    'recon2__3__FO': [78, 78, 78, 78, 78, 78, 78, 78, 78, 78],
    'recon2__6__GND': [2090, 2090, 2090, 2090, 2090, 2090, 2090, 2090, 2090, 2090],
    'recon2__6__FO': [78, 78, 78, 78, 78, 78, 78, 78, 78, 78],
    'tiago_fetch__d1__GND': [1036, 1036, 1036, 1036, 1036, 1036, 1036, 1036, 1036, 1036],
    'tiago_fetch__d1__FO': [56, 56, 56, 56, 56, 56, 56, 56, 56, 56],
    'tiago_fetch__d2__GND': [11088, 11088, 11088, 11088, 11088, 11088, 11088, 11088, 11088, 11088],
    'tiago_fetch__d2__FO': [56, 56, 56, 56, 56, 56, 56, 56, 56, 56],
    'tiago_hri__1__GND': [2173, 2173, 2173, 2173, 2173, 2173, 2173, 2173, 2173, 2173],
    'tiago_hri__1__FO': [138, 138, 138, 138, 138, 138, 138, 138, 138, 138],
    # 'tiago_hri__2__GND': [32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760],
    # 'tiago_hri__2__FO': [162, 162, 162, 162, 162, 162, 162, 162, 162, 162],
    'tiago_hri__3__GND': [32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760, 32760],
    'tiago_hri__3__FO': [162, 162, 162, 162, 162, 162, 162, 162, 162, 162],
    'triangle_tireworld__3__GND': [7744, 7744, 7744, 7744, 7744, 7744, 7744, 7744, 7744, 7744],
    'triangle_tireworld__3__FO': [38, 38, 38, 38, 38, 38, 38, 38, 38, 38],
    'triangle_tireworld__6__GND': [47212, 47212, 47212, 47212, 47212, 47212, 47212, 47212, 47212, 47212],
    'triangle_tireworld__6__FO': [38, 38, 38, 38, 38, 38, 38, 38, 38, 38],
    'turtlebot_survey__de2__GND': [540, 540, 540, 540, 540, 540, 540, 540, 540, 540],
    'turtlebot_survey__de2__FO': [137, 137, 137, 137, 137, 137, 137, 137, 137, 137],
    'turtlebot_survey__de4__GND': [1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700, 1700],
    'turtlebot_survey__de4__FO': [137, 137, 137, 137, 137, 137, 137, 137, 137, 137],
}

plot_data = {}


def list_addition(list1, list2):
    zipped = zip(list1, list2)
    result = []
    for v1, v2 in zipped:
        result.append(v1+v2)
    return result


def list_substraction(list1, list2):
    zipped = zip(list1, list2)
    result = []
    for v1, v2 in zipped:
        result.append(v1-v2)
    return result



x = range(1, 10+1)
index = 0
subplot_x = 0
subplot_y = 0
fig, ax = plt.subplots(2, 3, figsize=(8, 4))
plt.setp(ax, xticks=[2, 4, 6, 8, 10])


for domain in domain_order:
    problems = []
    # plot MBFS
    for problem, values in mbfs_num_base_features.items():
        if domain in problem:
            problems.append(problem)
            ax[subplot_x][subplot_y].title.set_text(domain_name[domain_order.index(domain)])
            if  'recon2__3' in problem or \
                'academic_advising__3' in problem or \
                'triangle_tireworld__3' in problem or \
                'turtlebot_survey__de2' in problem or \
                'tiago_fetch__d1' in problem or \
                'tiago_hri__1' in problem:
                legend_label = 'Small, MBFS'
                linestyle = '-'
            else:
                legend_label = 'Large, MBFS'
                linestyle = ':'
            if 'FO' in problem:
                legend_label += ', FO'
            else:
                legend_label += ', GND'
            ax[subplot_x][subplot_y].plot(x, values, linestyle=linestyle, linewidth=2, label=legend_label)
            ax[subplot_x][subplot_y].set_yscale('log')
            if subplot_x == 1:
                ax[subplot_x][subplot_y].set(xlabel = r'$\nu$')
            if subplot_y == 0:
                ax[subplot_x][subplot_y].set(ylabel = 'Num. of Base Features')
    # plot MFFS
    for problem in problems:
        if  'recon2__3' in problem or \
            'academic_advising__3' in problem or \
            'triangle_tireworld__3' in problem or \
            'turtlebot_survey__de2' in problem or \
            'tiago_fetch__d1' in problem or \
            'tiago_hri__1' in problem:
            legend_label = 'Small, MFFS'
        else:
            legend_label = 'Large, MFFS'
        if 'FO' in problem:
            legend_label += ', FO'
        else:
            legend_label += ', GND'
        ax[subplot_x][subplot_y].plot(x, mffs_num_base_features[problem], linestyle='-.', linewidth=2, label=legend_label)
    subplot_y += 1
    if subplot_y > 2:
        subplot_y = 0
        subplot_x += 1
fig.tight_layout()
plt.legend(ncol=4, loc='upper center', bbox_to_anchor=(-0.85, -0.3), framealpha=0.0)
plt.savefig('result-num-base-features.png', format='png', bbox_inches="tight", dpi=300)
