#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvin

This script computes the probability of a probabilistic effect being true in T time steps.
Given state fluent f has a probability p of being true in each time step, the probability P of f being true in time step T is:
P = sum_{t = 1 : T} p(1-p)^(t-1)
"""

p = 0.5
T = 10

P = 0
for t in range(T):
    t += 1
    P += p*(1-p)**(t-1)
    print('Time ' + str(t) + ': probability = ' + str(P))