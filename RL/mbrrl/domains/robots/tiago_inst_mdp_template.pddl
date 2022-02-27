(define (problem task)
(:domain tiago_mdp)
(:objects 
    r1 - robot 
    wp0 wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 - waypoint 
    p1 p2 p3 p4 - person 
    o1 o2 o3 o4 o5 o6 o7 o8 o9 o10 - obj
)
(:init
    (robot_at r1 wp0)
    (object_at o1 wp1)
    (object_at o2 wp2)
    (emptyhand r1)

    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (holding r1 o1)
    (localised r1)
    ; (explored ?v - robot)
    (object_with o1 p1)
    (person_found p1)
    (person_at p1 wp4)
    ; (person_satisfied p1)
    (task_received p1)
    (task_completed p1)
    (reward_received p1)
)
; add predicates that are non-fluents as constants, this will be parsed by LFIT and printed correctly as non-fluent in cpfs
(:constants
)
(:goal (and
    (reward_received p1)
))
  ;(:goal-reward 1)
  ;(:metric maximize (reward))
)