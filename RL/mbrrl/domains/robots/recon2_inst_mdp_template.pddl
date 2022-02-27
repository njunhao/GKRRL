(define (problem task)
(:domain recon2_mdp)
(:objects
    wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 wp10 wp11 wp12 wp13 wp14 wp15 wp16 wp17 wp18 wp19 wp20 wp21 wp22 wp23 wp24 wp25 - pos
    o0 o1 o2 o3 o4 o5 o6 - obj
    a1 - agent
    w1 l1 p1 - tool
)
(:constants
    (ADJACENT wp1 wp2)
    (ADJACENT wp1 wp6)
    (ADJACENT wp2 wp3)
    (ADJACENT wp2 wp7)
    (ADJACENT wp3 wp4)
    (ADJACENT wp3 wp8)
    (ADJACENT wp4 wp5)
    (ADJACENT wp4 wp9)
    (ADJACENT wp5 wp10)
    (ADJACENT wp6 wp7)
    (ADJACENT wp6 wp11)
    (ADJACENT wp7 wp8)
    (ADJACENT wp7 wp12)
    (ADJACENT wp8 wp9)
    (ADJACENT wp8 wp13)
    (ADJACENT wp9 wp10)
    (ADJACENT wp9 wp14)
    (ADJACENT wp10 wp15)
    (ADJACENT wp11 wp12)
    (ADJACENT wp11 wp16)
    (ADJACENT wp12 wp13)
    (ADJACENT wp12 wp17)
    (ADJACENT wp13 wp14)
    (ADJACENT wp13 wp18)
    (ADJACENT wp14 wp15)
    (ADJACENT wp14 wp19)
    (ADJACENT wp15 wp20)
    (ADJACENT wp16 wp17)
    (ADJACENT wp16 wp21)
    (ADJACENT wp17 wp18)
    (ADJACENT wp17 wp22)
    (ADJACENT wp18 wp19)
    (ADJACENT wp18 wp23)
    (ADJACENT wp19 wp24)
    (ADJACENT wp20 wp25)
    (ADJACENT wp21 wp22)
    (ADJACENT wp23 wp24)
    (ADJACENT wp24 wp25)

    (ADJACENT wp2 wp1)
    (ADJACENT wp6 wp1)
    (ADJACENT wp3 wp2)
    (ADJACENT wp7 wp2)
    (ADJACENT wp4 wp3)
    (ADJACENT wp8 wp3)
    (ADJACENT wp5 wp4)
    (ADJACENT wp9 wp4)
    (ADJACENT wp10 wp5)
    (ADJACENT wp7 wp6)
    (ADJACENT wp11 wp6)
    (ADJACENT wp8 wp7)
    (ADJACENT wp12 wp7)
    (ADJACENT wp9 wp8)
    (ADJACENT wp13 wp8)
    (ADJACENT wp10 wp9)
    (ADJACENT wp14 wp9)
    (ADJACENT wp15 wp10)
    (ADJACENT wp12 wp11)
    (ADJACENT wp16 wp11)
    (ADJACENT wp13 wp12)
    (ADJACENT wp17 wp12)
    (ADJACENT wp14 wp13)
    (ADJACENT wp18 wp13)
    (ADJACENT wp15 wp14)
    (ADJACENT wp19 wp14)
    (ADJACENT wp20 wp15)
    (ADJACENT wp17 wp16)
    (ADJACENT wp21 wp16)
    (ADJACENT wp18 wp17)
    (ADJACENT wp22 wp17)
    (ADJACENT wp19 wp18)
    (ADJACENT wp23 wp18)
    (ADJACENT wp24 wp19)
    (ADJACENT wp25 wp20)
    (ADJACENT wp22 wp21)
    (ADJACENT wp24 wp23)
    (ADJACENT wp25 wp24)

    (WATER_TOOL w1)
    (LIFE_TOOL l1)
    (CAMERA_TOOL p1)
    (BASE wp9)
    (OBJECT_AT o0 wp12)
    (OBJECT_AT o1 wp5)
    (OBJECT_AT o2 wp14)
    (OBJECT_AT o3 wp17)
    (OBJECT_AT o4 wp11)
    (OBJECT_AT o5 wp23)
    (OBJECT_AT o6 wp20)
    (HAZARD wp1)

)
(:init
    (ADJACENT wp1 wp2)
    (ADJACENT wp1 wp6)
    (ADJACENT wp2 wp3)
    (ADJACENT wp2 wp7)
    (ADJACENT wp3 wp4)
    (ADJACENT wp3 wp8)
    (ADJACENT wp4 wp5)
    (ADJACENT wp4 wp9)
    (ADJACENT wp5 wp10)
    (ADJACENT wp6 wp7)
    (ADJACENT wp6 wp11)
    (ADJACENT wp7 wp8)
    (ADJACENT wp7 wp12)
    (ADJACENT wp8 wp9)
    (ADJACENT wp8 wp13)
    (ADJACENT wp9 wp10)
    (ADJACENT wp9 wp14)
    (ADJACENT wp10 wp15)
    (ADJACENT wp11 wp12)
    (ADJACENT wp11 wp16)
    (ADJACENT wp12 wp13)
    (ADJACENT wp12 wp17)
    (ADJACENT wp13 wp14)
    (ADJACENT wp13 wp18)
    (ADJACENT wp14 wp15)
    (ADJACENT wp14 wp19)
    (ADJACENT wp15 wp20)
    (ADJACENT wp16 wp17)
    (ADJACENT wp16 wp21)
    (ADJACENT wp17 wp18)
    (ADJACENT wp17 wp22)
    (ADJACENT wp18 wp19)
    (ADJACENT wp18 wp23)
    (ADJACENT wp19 wp24)
    (ADJACENT wp20 wp25)
    (ADJACENT wp21 wp22)
    (ADJACENT wp23 wp24)
    (ADJACENT wp24 wp25)

    (ADJACENT wp2 wp1)
    (ADJACENT wp6 wp1)
    (ADJACENT wp3 wp2)
    (ADJACENT wp7 wp2)
    (ADJACENT wp4 wp3)
    (ADJACENT wp8 wp3)
    (ADJACENT wp5 wp4)
    (ADJACENT wp9 wp4)
    (ADJACENT wp10 wp5)
    (ADJACENT wp7 wp6)
    (ADJACENT wp11 wp6)
    (ADJACENT wp8 wp7)
    (ADJACENT wp12 wp7)
    (ADJACENT wp9 wp8)
    (ADJACENT wp13 wp8)
    (ADJACENT wp10 wp9)
    (ADJACENT wp14 wp9)
    (ADJACENT wp15 wp10)
    (ADJACENT wp12 wp11)
    (ADJACENT wp16 wp11)
    (ADJACENT wp13 wp12)
    (ADJACENT wp17 wp12)
    (ADJACENT wp14 wp13)
    (ADJACENT wp18 wp13)
    (ADJACENT wp15 wp14)
    (ADJACENT wp19 wp14)
    (ADJACENT wp20 wp15)
    (ADJACENT wp17 wp16)
    (ADJACENT wp21 wp16)
    (ADJACENT wp18 wp17)
    (ADJACENT wp22 wp17)
    (ADJACENT wp19 wp18)
    (ADJACENT wp23 wp18)
    (ADJACENT wp24 wp19)
    (ADJACENT wp25 wp20)
    (ADJACENT wp22 wp21)
    (ADJACENT wp24 wp23)
    (ADJACENT wp25 wp24)

    (WATER_TOOL w1)
    (LIFE_TOOL l1)
    (CAMERA_TOOL p1)
    (BASE wp9)
    (OBJECT_AT o0 wp12)
    (OBJECT_AT o1 wp5)
    (OBJECT_AT o2 wp14)
    (OBJECT_AT o3 wp17)
    (OBJECT_AT o4 wp11)
    (OBJECT_AT o5 wp23)
    (OBJECT_AT o6 wp20)
    (HAZARD wp1)

    (agentAt a1 wp9)
    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (damaged w1)
    (waterChecked o1)
    (waterDetected o1)
    (lifeChecked o1)
    (lifeChecked2 o1)
    (lifeDetected o1)
)
(:goal (and
    (pictureTaken o1)
)))
