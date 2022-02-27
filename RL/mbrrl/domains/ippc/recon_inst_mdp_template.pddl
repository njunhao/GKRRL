(define (problem task)
(:domain recon_mdp)
(:objects
    x0 x1 x2 x3 x4 - x_pos
    y0 y1 y2 y3 y4 - y_pos
    o0 o1 o2 o3 o4 o5 o6 - obj
    a1 - agent
    l1 w1 p1 - tool
)
(:constants
    (ADJACENT-LEFT x0 x0)
    (ADJACENT-DOWN y0 y0)
    (ADJACENT-RIGHT x0 x1)
    (ADJACENT-UP y0 y1)
    (ADJACENT-LEFT x1 x0)
    (ADJACENT-DOWN y1 y0)
    (ADJACENT-RIGHT x1 x1)
    (ADJACENT-UP y1 y1)
    (WATER_TOOL w1)
    (LIFE_TOOL l1)
    (CAMERA_TOOL p1)
    (BASE x0 y1)
    (objAt o0 x1 y1)
    (objAt o1 x1 y0)
    (objAt o2 x0 y0)
    (objAt o3 x1 y0)
    (HAZARD x1 y0)
)
(:init
    (agentAt a1 x0 y1)
    ; add dummy predicate else this predicate will not be loaded into LFIT if it does not appear in domain precond/effect
    (damaged l1)
    (waterChecked o0)
    (waterDetected o0)
    (lifeChecked o0)
    (lifeChecked2 o0)
    (lifeDetected o0)
    (pictureTaken o0)
)
(:goal (and
)))
