(define (domain turtlebot_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
  waypoint 
  robot
)

(:predicates
  (robot_at ?v - robot ?loc - waypoint)
  (visited ?loc - waypoint)
  (undocked ?v - robot)
  (docked ?v - robot)
  (localised ?v - robot)
  (dock_at ?loc - waypoint)
)

;; Move to any waypoint, avoiding terrain
(:action move
  :parameters (?v - robot ?from ?to - waypoint)
  :precondition (and )
  :effect (and )
)

;; Localise
(:action localise
  :parameters (?v - robot)
  :precondition (and )
  :effect (and )
)

;; Dock to charge
(:action dock
  :parameters (?v - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

(:action undock
  :parameters (?v - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

)
