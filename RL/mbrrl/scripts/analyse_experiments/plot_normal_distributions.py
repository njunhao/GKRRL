#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

This plots the normal distribution of action's selection criteria using Thompson Sampling
"""



import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import sys

def parse_line(line):
	# line = '#7 N(-0.160956, 0.00826446) #19 N(-0.00334193, 0.00254453) #20 N(-0.000986773, 0.000739645) #21 N(-1.70308, 0.25) #22 N(-0.00465263, 0.0027027)'
	curves = []
	for phrase in line.split('#'):
		mu = phrase[phrase.find('N(')+2 : phrase.find(',')].strip()
		variance = phrase[phrase.find(',')+1 : phrase.find(')')].strip()
		if not mu or not variance:
			continue
		desc = phrase[: phrase.find('N')]
		curves.append((float(mu), float(variance), '#'+desc))
	return curves


if __name__ == "__main__":
	if len(sys.argv) == 1:
		raise Exception('./plot_normal_distributions.py [string]')
	curves = parse_line(sys.argv[1])
	for mu, variance, desc in curves:
		sigma = math.sqrt(variance)
		x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
		plt.plot(x, stats.norm.pdf(x, mu, sigma), label = desc)
	plt.legend()
	plt.show()
	

