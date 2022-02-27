(define (problem task)
(:domain turtlebot_survey_mdp)
(:objects
    r1 - robot
    wp0 wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 wp10 - waypoint
    o1 o2 o3 o4 o5 o6 o7 o8 o9 o10 - obj
)
(:constants
    (DOCK_AT wp0)
    (COMM_TOWER wp3)
    (OBJECT_AT o1 wp1)
    (OBJECT_AT o2 wp2)
    ; (COST_MOVE)
    ; (TASK_REWARD)
    ; (PROB_LOSING_LOCALISATION)
    ; (PROB_LOW_ENERGY)
    ; (PROB_SUCCESSFUL_SURVEY)
    ; (PROB_SUCCESSFUL_OBSERVATION)
    ; (PROB_SUCCESSFUL_SURVEY_DAMAGED)
    ; (PROB_SUCCESSFUL_OBSERVATION_DAMAGED)
)
(:init
    (DOCK_AT wp0)
    (COMM_TOWER wp3)
    ; (COST_MOVE)
    ; (TASK_REWARD)
    ; (PROB_LOSING_LOCALISATION)
    ; (PROB_LOW_ENERGY)
    ; (PROB_SUCCESSFUL_SURVEY)
    ; (PROB_SUCCESSFUL_OBSERVATION)
    ; (PROB_SUCCESSFUL_SURVEY_DAMAGED)
    ; (PROB_SUCCESSFUL_OBSERVATION_DAMAGED)

    (robot_at r1 wp0)
    (docked r1)
    (OBJECT_AT o1 wp1)
    (OBJECT_AT o2 wp2)
    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (undocked r1)
    (localised r1)
    (object_found r1 o1)
    (object_inspected r1 o1)
    (camera_calibrated r1)
    (has_energy r1)
    (low_energy r1)
)
(:goal (and
    (object_info_received o1)
    (object_info_received o2)
    (reward_received o1)
    (reward_received o2)

)))
