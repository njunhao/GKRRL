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
  :precondition (and (robot_at ?v ?from) (localised ?v) (undocked ?v))
  :effect (and (visited ?to) (robot_at ?v ?to) (not (robot_at ?v ?from)))
)

;; Localise
(:action localise
  :parameters (?v - robot)
  :precondition (undocked ?v)
  :effect (localised ?v)
)

;; Dock to charge
(:action dock
  :parameters (?v - robot ?loc - waypoint)
  :precondition (and
    (dock_at ?loc)
    (robot_at ?v ?loc)
    (undocked ?v))
  :effect (and (docked ?v) (not (undocked ?v)))
)

(:action undock
  :parameters (?v - robot ?loc - waypoint)
  :precondition (and
    (dock_at ?loc)
    (docked ?v))
  :effect (and
    (not (docked ?v))
    (undocked ?v))
)

)
