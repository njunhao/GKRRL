(define (domain turtlebot_goal_mdp)

(:requirements :strips :typing :disjunctive-preconditions );:probabilistic-effects)

(:types
  waypoint 
  robot
)

(:predicates
  (COST_MOVE ?v - robot)
  (VISIT_WP_REWARD)
  (goal_reached)
  (robot_at ?v - robot ?loc - waypoint)
  (visited ?loc - waypoint)
  (undocked ?v - robot)
  (docked ?v - robot)
  (localised ?v - robot)
  (DOCK_AT ?loc - waypoint)
)

;; Move to any waypoint, avoiding terrain
(:action move
  :parameters (?v - robot ?from - waypoint ?to - waypoint)
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
