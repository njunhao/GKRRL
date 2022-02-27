#!/bin/bash
# arg1: directory for prost/testbed
# arg2: benchmark directory (required input)
# arg3: portnumber
# arg4: number of rounds
# arg5: random seed
# arg6: use timeout (0/1 for false/true)
# arg7: individual session (0/1 for false/true)
# arg8: log folder
# arg9: monitor execution (0/1 for false/true)
# arg10: class name for visualization display (i.e., rddlsim screen display class)

HOME_DIR="/media/alvin/HDD/Academics/PhD/Coding/Planners/prost/testbed"
# BENCHMARK_DIR="/media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/domains/benchmarks/ippc-all/rddl"
BENCHMARK_DIR="/media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/domains/robots"

PORT=2323
NUM_ROUNDS=5
SEED=1
TIMEOUT=0
IND_SESSION=0
LOG_DIR="/media/alvin/HDD/Academics/PhD/Coding/RL/mbrrl/results/current"
MONITOR_EXEC=1

./run-server ${HOME_DIR} ${BENCHMARK_DIR} ${PORT} ${NUM_ROUNDS} ${SEED} ${TIMEOUT} ${IND_SESSION} ${LOG_DIR} ${MONITOR_EXEC}