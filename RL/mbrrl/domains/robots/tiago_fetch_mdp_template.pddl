(define (domain tiago_fetch_mdp)
(:requirements :strips :typing ) ;;probabilistic-effects  )
(:types waypoint robot obj)
(:predicates
  ; (TASK_REWARD)
  ; (COST)
  ; (PROB_LOSING_LOCALISATION ?v - robot)
  (robot_at ?v - robot ?loc - waypoint)
  (localised ?v - robot)
  (emptyhand ?v - robot)
  (holding ?v - robot ?o - obj)
  (poor_grasp ?v - robot ?o - obj)
  (object_at ?o - obj ?loc - waypoint)
  (OBJECT_GOAL ?o - obj ?loc - waypoint)
)

;; Move to any waypoint, avoiding terrain
(:action move
  :parameters (?v - robot ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

;; Localise
(:action localise
  :parameters (?v - robot)
  :precondition (and )
  :effect (and )
)

;; pick up object
(:action pick_up
  :parameters (?v - robot ?o - obj ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

;; put down object
(:action put_down
  :parameters (?v - robot ?o - obj ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

;; explore
; (:action explore
;   :parameters (?v - robot)
;   :precondition (and (localised ?v))
;   :effect (and (explored ?v))
; )

)