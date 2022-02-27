#!/bin/bash
# Call by run_ros_experiments.py to run ROS experiments in tmux

if [ $# -lt 2 ]
then
    echo "Need at least 3 arguments: [mode = run, rerun, kill] [experiments_settings_xxx] [port num xxxx] <skip first few experiments>"
    exit
fi

# start tmux session for server if session doesn't exist
tmux has-session -t s$3 2>/dev/null
if [ $? != 0 ]; then
    echo "Create new tmux session: s$3"
    tmux new-session -d -s s$3
    wait
    tmux send -t s$3 "cd /home/alvin/Downloads/Bash/" ENTER
    wait
    tmux send -t s$3 "export PATH=/home/alvin/.local/bin:/opt/ros/kinetic/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin" ENTER
    wait
    tmux send -t s$3 ". rosplan.sh" ENTER
    wait
fi

# start tmux session for client if session doesn't exist
tmux has-session -t c$3 2>/dev/null
if [ $? != 0 ]; then
    echo "Create new tmux session: c$3"
    tmux new-session -d -s c$3
    wait
    tmux send -t c$3 "cd /home/alvin/Downloads/Bash/" ENTER
    wait
    tmux send -t c$3 ". mbrrl.sh" ENTER
    wait
fi

# send a string to console of tmux session
# need ENTER at the end which is equivalent to pressing the ENTER key to run command
if [ $# -lt 4 ]
then
    echo "Killing tmux session s$3"
    tmux send -t s$3 "C-c" ENTER
    wait
    echo "Killing tmux session c$3"
    tmux send -t c$3 "C-c" ENTER
    wait
    if [ $1 = "run" ] || [ $1 = "rerun" ]
    then
        if [ $1 = "rerun" ]
        then
            sleep 60
        fi
        echo "Running experiments"
        tmux send -t c$3 "python3 run_experiments.py $2 client -port $3" ENTER
        wait
        sleep 5
        tmux send -t s$3 "python3 run-ros-experiments.py" ENTER
    fi
elif [ $# -lt 5 ]
then
    echo "Killing tmux session s$3"
    tmux send -t s$3 "C-c" ENTER
    wait
    echo "Killing tmux session c$3"
    tmux send -t c$3 "C-c" ENTER
    wait
    if [ $1 = "run" ] || [ $1 = "rerun" ]
    then
        if [ $1 = "rerun" ]
        then
            sleep 60
        fi
        echo "Running experiments"
        tmux send -t c$3 "python3 run_experiments.py $2 client -port $3 -skip_experiments $4" ENTER
        wait
        sleep 5
        tmux send -t s$3 "python3 run-ros-experiments.py" ENTER
    fi
fi