(define (domain recon_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
    x_pos
    y_pos
    obj
    agent
    tool
)

(:predicates
  (ADJACENT-UP ?y1 - y_pos ?y2 - y_pos)
  (ADJACENT-DOWN ?y1 - y_pos ?y2 - y_pos)
  (ADJACENT-RIGHT ?x1 - x_pos ?x2 - x_pos)
  (ADJACENT-LEFT ?x1 - x_pos ?x2 - x_pos)
  (objAt ?o - obj ?x - x_pos ?y - y_pos)
  (HAZARD ?x - x_pos ?y - y_pos)
  (CAMERA_TOOL ?t - tool)
  (LIFE_TOOL ?t - tool)
  (WATER_TOOL ?t - tool)
  (BASE ?x - x_pos ?y - y_pos)
  (damaged ?t - tool)
  (waterChecked ?o - obj)
  (waterDetected ?o - obj)
  (lifeChecked ?o - obj)
  (lifeChecked2 ?o - obj)
  (lifeDetected ?o - obj)
  (pictureTaken ?o - obj)
  (agentAt ?a - agent ?x - x_pos ?y - y_pos)
)

; (:action up
;   :parameters (?a - agent)
;   :precondition (and )
;   :effect (and )
; )

; (:action down
;   :parameters (?a - agent)
;   :precondition (and )
;   :effect (and )
; )

; (:action left
;   :parameters (?a - agent)
;   :precondition (and )
;   :effect (and )
; )

; (:action right
;   :parameters (?a - agent)
;   :precondition (and )
;   :effect (and )
; )

(:action useToolOn
  :parameters (?a - agent ?t - tool ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action repair
  :parameters (?a - agent ?t - tool)
  :precondition (and )
  :effect (and )
)

)