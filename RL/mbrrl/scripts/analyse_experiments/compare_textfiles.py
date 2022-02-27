#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

Compares the differences in contents of text files
"""


from pathlib import Path

files = [
	'/media/alvin/HDD/New/todo/results_RI/robot_inspection_0001/learned_domain.rddl',
	'/media/alvin/HDD/New/todo/results_RI/robot_inspection_0002/learned_domain.rddl',
	'/media/alvin/HDD/New/todo/results_RI/robot_inspection_0003/learned_domain.rddl',
]
file_contents = []

for file in files:
	file_contents.append((file, Path(file).read_text()))

for i in range(len(file_contents)):
	for j in range(i, len(file_contents)):
		if file_contents[i][1] != file_contents[j][1]:
			print(file_contents[i][0] + ' mismatch ' + file_contents[j][0])
	print('')
