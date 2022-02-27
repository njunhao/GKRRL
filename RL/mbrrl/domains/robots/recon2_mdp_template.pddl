(define (domain recon2_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
  pos 
  obj
  agent
  tool
)

(:predicates
  (GOOD_PIC_WEIGHT)
  (BAD_PIC_WEIGHT)
  (DETECT_PROB)
  (DETECT_PROB_DAMAGE)
  (DAMAGE_PROB ?t - tool)

  (ADJACENT ?from - pos ?to - pos)  
  (OBJECT_AT ?o - obj ?loc - pos)
  (HAZARD ?loc - pos)
  (CAMERA_TOOL ?t - tool)
  (LIFE_TOOL ?t - tool)  
  (WATER_TOOL ?t - tool) 
  (BASE ?loc - pos)
  (damaged ?t - tool)
  (waterChecked ?o - obj) 
  (waterDetected ?o - obj)
  (lifeChecked ?o - obj) 
  (lifeChecked2 ?o - obj)
  (lifeDetected ?o - obj)
  (pictureTaken ?o - obj)
  (agentAt ?a - agent ?loc - pos)
)

(:action move
  :parameters (?a - agent ?loc - pos)
  :precondition (and )
  :effect (and )
)

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