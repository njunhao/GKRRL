# GK-RRL+
## Generalised-Knowledge-Assisted+ Relational Reinforcement Learning 

**Author**: NG Jun Hao, Alvin

**Institution**: Edinburgh Centre for Robotics

**Description**: This repository contains software created during my PhD along with some publicly available libraries, some of which have been modified by me.

**Tested on**: Ubuntu 16.04, Python 3.6.3

**License**: MIT

## Installation
Download the software at [Github](https://github.com/njunhao/GKRRL). It contains all the files required to run the experiments. Extract the binary located in /run_mbrrl/RL/mbrrl/src/mbrrl.zip to the same directory (i.e., /run_mbrrl/RL/mbrrl/src/mbrrl)

## Setting up experiments
The setting file for the experiments is */run_mbrrl/RL/mbrrl/scripts/run_experiments/experiments_settings_X.py*
There are a lot of settings, these are the main ones:
- num_reps (number of repetitions, the random seed will be automaticaly incremented by one)
- num_rounds (number of episodes per repetition)
- problems (format is (domain, problem instance))
- setting_choice (this initalises a set of predefined parameters to run a certain type of experiment)
-- *setting_choice = transfer_learning* will run transfer learning experiments

For transfer learning, make sure *import_knowledge_folder* and *import_knowledge_folder_lfd* is defined correctly. You need the Q-function approximations (*qvalue_approximation.dat*) and/or first-order dead end situations (*tabu.dat*). These files are produced by learning from scratch first.

**Verbose:**

Try to test the *verbose flags* with a small number of episodes to see what they do. They can print out quite a bit of stuff, racking up tens of gigabyte of memory in minutes. The larger the number, the more verbose it gets.

**Linear function approximation:**

*GND_APPROX* defines the ground approximation (do not edit)

*CX_BASIC* defines the first-order approximation and various combinations of contextual knowledge. There are 24 predefined combinations which you can try out.

**New setting file:**

You can create your own setting file as long as it follows this naming convention: */run_mbrrl/RL/mbrrl/scripts/run_experiments/experiments_settings_<setting file>.py*



## Running experiments
You need two terminals to run experiments. Both terminals need to run the server and client concurrently as they communicate via TCP.

### Run the server (rddlsim)
**First Tab:**

```sh
cd /run_mbrrl/RL/mbrrl/scripts/run_experiments
./run_experiments.py <setting file> server -port <port num>
```

**Example:**

```sh
cd /run_mbrrl/RL/mbrrl/scripts/run_experiments
./run_experiments.py example server -port 2323
```

This will load */run_mbrrl/RL/mbrrl/scripts/run_experiments/experiments_settings_example.py*.


### Run the client (GK-RRL+)

**Second Tab:**

```sh
cd /run_mbrrl/RL/mbrrl/scripts/run_experiments
./run_experiments.py <setting file> client -port <port num> -problem <problem num> -lfa <LFA num>
```

**Example:**
```sh
cd /run_mbrrl/RL/mbrrl/scripts/run_experiments
./run_experiments.py <setting file> client -port 2323 -problem 0 -lfa 1
```

This will run the first problem instance in *problems* and the second configuration of *function_approximations*.

Port number must be the same for both terminals.

*<problem num>* is the problem instance to run (*problems[problem num]* where *problems* is defined in *experiments_settingss_<setting file>.py*)

*<LFA num>* is the configuration of the linear function approximation to use (function_approximations[LFA num] where *function_approximations* is defined in *experiments_settings_<setting file>.py*)

All arguments are optional. By default, the port num is *2323* and all combinations of problem instances and linear function approximations will run.

**Files to run experiments:**

Domain and problem RDDL files will be copied to */run_mbrrl/RL/mbrrl/domains/experiments-<port num>* to avoid modifying the original files. A copy of the binary will also be created as */run_mbrrl/RL/mbrrl/src/mbrrl-<port num>*. You can delete these files once the experiments are done.


**Logfiles:**

Results will be saved to */run_mbrrl/RL/mbrrl/results-<port num>*

*mbrrl.log* contains the results, it is the most important file and should not be deleted.

*mbrrl_console.log* is the detailed log file which you can read to understand what the algorithm is doing.

*qvalue_approximation.dat* is the Q-function which can be imported for transfer learning.

*tabu.dat* is the (first-order) dead end situations which can be imported for transfer learning.


## Plot Results
Results will be saved to */run_mbrrl/RL/mbrrl/results-<port num>*

You can rename this folder and move it to another directory. 

To plot the results, first:
```sh
cd /run_mbrrl/RL/mbrrl/scripts/analyse_experiments
```

To plot results in */run_mbrrl/RL/mbrrl/results-<port num>*:
```sh
python3 batch-plot.py <port num>
```

Or to plot results in any directory:
```sh
python3 batch-plot.py <directory>
```

Or to compare results from multiple directories:
```sh
python3 batch-plot.py <directory> <directory> <directory> <directory>
```

The file you may want to edit is */run_mbrrl/RL/mbrrl/scripts/analyse_experiments/batch_plot.py*

You shouldn't need to edit any other files. There is a lot to *batch_plot.py* but a simple use is to edit:

- settings['folders_to_analyse']
    - This is a list of strings for each directory holding the logfile (*mbrrl.log*) you wish to plot for
    - For example, if *mbrrl.log* is in */dir/<domain>/experiment_<domain>_doubleq_epsilon_0001*, then *settings['folders_to_analyse'] = /dir/*
- settings['plot_options']
    - For example, to plot total undiscounted rewards, uncomment the line *settings['plot_options'].append(['rewards', 'terminal', 'cross'])*
- settings['generic_plot_options']
    - Some options to alter figure appearance
- settings['plot_settings']
    - Some options to alter figure appearance

Legends are automatically generated and can be lengthy. You will have to manually overwrite the legends by editing *settings['legend_labels']*


## Add new domains and problems

**Step 1:**

Add .rddl files to */run_mbrrl/RL/mbrrl/domains/robots*

**Step 2:**

Edit */run_mbrrl/RL/mbrrl/scripts/run_experiments/domains_utils.py*

**Example:**
```sh
lsof_domains.add(Domain(
    **{'name': 'academic_advising',
       'folder': exp_utils.mbrrl_path + '/domains/ippc',
       'rpg_folder': None,
       'approx': None,
       'empty': exp_utils.mbrrl_path + '/domains/ippc_incomplete/academic_advising_mdp_empty.rddl'}))
```

The algorithm is not guaranteed to work for new domains as the terminal states, goal context, and location context are hardcoded for each domain.


## Note

Domain names are different from the dissertation.

In dissertation (repository):
- recon                           (recon2)
- robot_fetch                     (tiago_fetch)
- robot_inspection                (turtlebot_survey)
- service_robot                   (tiago_hri)

Problem instance names are different from the dissertation.
In dissertation (repository):
- robot_fetch (tiago_fetch)
    - 1 (d1)
-- 2 (d2)
- robot_inspection (turtlebot_survey)
    - 1 (de2)
    - 2 (de4)