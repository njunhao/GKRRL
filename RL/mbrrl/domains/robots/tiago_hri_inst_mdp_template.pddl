(define (problem task)
(:domain tiago_hri_mdp)
(:objects wp0 wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 - waypoint r1 - robot p1 p2 p3 - person o1 o2 o3 o4 o5 o6 - obj)
(:init
    ; (TASK_REWARD)
    ; (COST)
    ; (PROB_LOSING_LOCALISATION r1)
    (robot_at r1 wp0)
    (object_at o1 wp1)
    (object_at o2 wp2)
    (emptyhand r1)

    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (holding r1 o1)
    (localised r1)
)
; add predicates that are non-fluents as constants, this will be parsed by LFIT and printed correctly as non-fluent in cpfs
(:constants
    (TABLE_AT wp1)
    (PERSON_GOAL_OBJECT_AT p1 o1 wp2)
    (PERSON_GOAL_OBJECT_WITH p3 o5 p1)
    (PERSON_IS_AT p1 wp4)
)
(:goal (and
    ; (reward_received o1)
    (object_at o1 wp0)
    (object_with o5 wp1)
))
  ;(:goal-reward 1)
  ;(:metric maximize (reward))
)