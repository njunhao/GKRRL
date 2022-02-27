(define (domain robot_inspection_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
  pos 
  robot
  obj
)

(:predicates
  (COST)
  (TASK_REWARD)
  (PROB_DAMAGE)
  (PROB_SUCCESSFUL_SURVEY)
  (PROB_SUCCESSFUL_OBSERVATION)
  (PROB_SUCCESSFUL_SURVEY_DAMAGED)
  (PROB_SUCCESSFUL_OBSERVATION_DAMAGED)

  (ADJACENT ?loc - pos ?loc - pos)
  (HAZARD ?loc - pos ?loc - pos)
  (BASE ?loc - pos)
  (COMM_TOWER ?loc - pos)
  (OBJECT_AT ?o - obj ?loc - pos)
  (robot_at ?r - robot ?loc - pos)
  (object_found ?o - obj)
  (object_inspected ?o - obj)
  (object_info_received ?o - obj)
  (camera_damaged ?r - robot)
  (camera_calibrated ?r - robot)
)

(:action move
  :parameters (?r - robot ?loc - pos)
  :precondition (and )
  :effect (and )
)

(:action survey
  :parameters (?r - robot ?loc - pos)
  :precondition (and )
  :effect (and )
)

(:action inspect_object
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action transmit_info
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

(:action calibrate_camera
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

)