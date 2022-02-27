(define (domain husky_inspection_mdp)
(:requirements :strips :typing ) ;;probabilistic-effects  )
(:types waypoint robot obj)
(:predicates
  ; (TASK_REWARD)
  ; (COST_MOVE ?r - robot)
  ; (COST_LOCATE_POI ?r - robot)
  ; (COST_INSPECT_POI ?r - robot)
  ; (COST_TAKE_IMAGE ?r - robot)
  ; (COST_MANIPULATE_VALVE ?r - robot)
  ; (COST_REPAIR_CAMERA ?r - robot)
  ; (COST_REPAIR_MANIPULATOR ?r - robot)

  ; (PROB_LOCALISED ?r - robot)
  ; (PROB_FOUND_DAMAGED ?r - robot ?obj - obj)
  ; (PROB_FOUND ?r - robot ?obj - obj)
  ; (PROB_INSPECTED_DAMAGED ?r - robot ?obj - obj)
  ; (PROB_INSPECTED ?r - robot ?obj - obj)
  ; (PROB_IMAGE_TAKEN_DAMAGED ?r - robot ?obj - obj)
  ; (PROB_IMAGE_TAKEN ?r - robot ?obj - obj)
  ; (PROB_VALVE_TURNED_DAMAGED ?r - robot ?obj - obj)
  ; (PROB_VALVE_TURNED ?r - robot ?obj - obj)
  ; (PROB_DAMAGED_MANIPULATOR ?r - robot)
  ; (PROB_DAMAGED_CAMERA ?r - robot)

  (GOAL_POI_INSPECTED ?obj - obj)
  (GOAL_VALVE_TURNED ?obj - obj)
  (GOAL_POI_IMAGE_TAKEN ?obj - obj)
  ; (close_to ?loc1 - ?loc2 - waypoint)
  (POI_AT ?obj - obj ?loc - waypoint)
  (BASE ?loc - waypoint)
  (VALVE_AT ?obj - obj)

  (at ?r - robot ?loc - waypoint)
  (localised ?r - robot)
  (poi_found ?r - robot ?obj - obj)
  (poi_inspected ?r - robot ?obj - obj)
  (poi_image_taken ?r - robot ?obj - obj)
  (poi_valve_turned ?r - robot ?obj - obj)
  (damaged_manipulator ?r - robot)
  (damaged_camera ?r - robot)
  (reward_received_for_inspection ?obj - obj)
  (reward_received_for_manipulation ?obj - obj)
  (reward_received_for_image_taken ?obj - obj)
)

(:action move
  :parameters (?r - robot ?from ?to - waypoint)
  :precondition (and )
  :effect (and )
)

(:action localise
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

(:action locate_poi
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action inspect_poi
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action take_image
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action manipulate_valve
  :parameters (?r - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

(:action repair_manipulator
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

(:action repair_camera
  :parameters (?r - robot)
  :precondition (and )
  :effect (and )
)

)