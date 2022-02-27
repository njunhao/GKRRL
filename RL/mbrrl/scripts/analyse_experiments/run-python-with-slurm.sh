#!/bin/bash
# Run run_experiments.py using bash script (needed to run jobs on servers)

GPU="gpu0"

if [ $# -lt 2 ]
then
  echo "Need at least 2 arguments: [gpu num] [tmux session num] [path of python script]"
  exit
fi

# start tmux session if session doesn't exist
tmux has-session -t $2 2>/dev/null
if [ $? != 0 ]; then
  echo "Create new tmux session: $2"
  tmux new-session -d -s $2
  wait
fi

# send a string to console of tmux session
# need ENTER at the end which is equivalent to pressing the ENTER key to run command
# tmux send -t $2 "srun --partition=amd-longq --nodelist=$GPU$1 python3 "${@:3}"" ENTER
tmux send -t $2 "srun --partition=amd-longq --nodelist=$GPU$1 python3 /home/nalvin/rrl/run_mbrrl/RL/mbrrl/scripts/analyse_experiments/list_files_count_in_experiment_folders.py /scratch/nalvin" ENTER