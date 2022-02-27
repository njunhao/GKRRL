(define (problem task)
(:domain tiago_fetch_mdp)
(:objects wp0 wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 wp10 wp11 wp12 - waypoint r1 - robot o1 o2 o3 o4 o5 o6 o7 o8 o9 o10 - obj)
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
    (poor_grasp r1 o1)
    (localised r1)
)
; add predicates that are non-fluents as constants, this will be parsed by LFIT and printed correctly as non-fluent in cpfs
(:constants
    (OBJECT_GOAL o1 wp0)
)
(:goal (and
    ; (reward_received o1)
    (object_at o1 wp0)
))
  ;(:goal-reward 1)
  ;(:metric maximize (reward))
)