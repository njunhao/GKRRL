(define (problem task)
(:domain robot_inspection_mdp)
(:objects
    r1 - robot
    wp1 wp2 wp3 wp4 - pos
    o0 o1 - obj
)
(:constants
    (ADJACENT wp1 wp2)
    (ADJACENT wp1 wp3)
    (ADJACENT wp2 wp4)
    (ADJACENT wp3 wp4)

    (ADJACENT wp2 wp1)
    (ADJACENT wp3 wp1)
    (ADJACENT wp4 wp2)
    (ADJACENT wp4 wp3)

    (HAZARD wp1 wp3)
    
    (HAZARD wp3 wp1)

    (BASE wp4)
    (COMM_TOWER wp1)
    (OBJECT_AT o0 wp2)
    (OBJECT_AT o1 wp3)
)
(:init
    (ADJACENT wp1 wp2)
    (ADJACENT wp1 wp3)
    (ADJACENT wp2 wp4)
    (ADJACENT wp3 wp4)

    (ADJACENT wp2 wp1)
    (ADJACENT wp3 wp1)
    (ADJACENT wp4 wp2)
    (ADJACENT wp4 wp3)

    (HAZARD wp1 wp3)
    
    (HAZARD wp3 wp1)

    (BASE wp4)
    (COMM_TOWER wp1)
    (OBJECT_AT o0 wp2)
    (OBJECT_AT o1 wp3)

    (robot_at r1 wp1)
    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (object_found o1)
    (object_inspected o1)
    (camera_damaged r1)
    (camera_calibrated r1)
)
(:goal (and
    (object_info_received o0)
    (object_info_received o1)
)))
