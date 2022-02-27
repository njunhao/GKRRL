(define (domain turtlebot_survey_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
  waypoint 
  robot
  obj
)

(:predicates
  (COST_MOVE)
  (COST_LOCALISE)
  (COST_DOCK)
  (COST_UNDOCK)
  (COST_SURVEY)
  (COST_INSPECTION)
  (COST_TRANSMIT)
  (COST_CALIBRATE)
  (TASK_REWARD)
  (PROB_LOSING_LOCALISATION)
  (PROB_LOW_ENERGY)
  (PROB_SUCCESSFUL_SURVEY)
  (PROB_SUCCESSFUL_OBSERVATION)
  (PROB_SUCCESSFUL_SURVEY_DAMAGED)
  (PROB_SUCCESSFUL_OBSERVATION_DAMAGED)

  (DOCK_AT ?loc - waypoint)
  (COMM_TOWER ?loc - waypoint)
  (OBJECT_AT ?o - obj ?loc - waypoint)
  (robot_at ?r - robot ?loc - waypoint)
  (undocked ?r - robot)
  (docked ?r - robot)
  (localised ?r - robot)
  (object_found ?r - robot ?o - obj)
  (object_inspected ?r - robot ?o - obj)
  (object_info_received ?o - obj)
  (camera_calibrated ?r - robot)
  (has_energy ?r - robot)
  (low_energy ?r - robot)
  (reward_received ?o - obj)
)


(:action move
  :parameters (?r - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action localise
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

(:action dock
  :parameters (?r - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action undock
  :parameters (?r - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action survey
  ; :parameters (?r - robot)
  :parameters (?r - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action inspect_object
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action transmit_info
  :parameters (?r - robot) ; ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action calibrate_camera
  :parameters (?r - robot) ; ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

)