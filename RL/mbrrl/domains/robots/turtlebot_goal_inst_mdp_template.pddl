(define (problem task)
(:domain turtlebot_goal_mdp)
(:objects
    wp0 wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 wp10 - waypoint
    r1 - robot
)
(:constants
    (DOCK_AT wp0)
    (COST_MOVE r1)
    (VISIT_WP_REWARD)
)
(:init
    (robot_at r1 wp0)
    (docked r1)
    (DOCK_AT wp0)
    (COST_MOVE r1)
    (VISIT_WP_REWARD)
    (goal_reached)
    (undocked r1)  ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (localised r1) ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (visited wp0)     ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
)
(:goal (and
    (visited wp0)
    (visited wp1)
    (visited wp2)
    (visited wp3)
    (visited wp4)
    (docked r1)
)))
