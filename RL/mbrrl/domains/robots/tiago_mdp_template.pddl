(define (domain tiago_mdp)
(:requirements :strips :typing ) ;;probabilistic-effects  )
(:types waypoint robot obj person)
(:predicates
  (robot_at ?v - robot ?loc - waypoint)
  (localised ?v - robot)
  ; (explored ?v - robot)
  (emptyhand ?v - robot)
  (holding ?v - robot ?o - obj)
  (object_at ?o - obj ?loc - waypoint)
  (object_with ?o - obj ?p - person)
  (person_found ?p - person)
  (person_at ?p - person ?loc - waypoint)
  ; (person_satisfied ?p - person)
  (task_received ?p - person)
  (task_completed ?p - person)
  (reward_received ?p - person)
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

; find person
(:action find_person
  :parameters (?v - robot ?p - person)
  :precondition (and )
  :effect (and )
)

;; ask person
(:action talk_to_person
  :parameters (?v - robot ?p - person ?loc - waypoint)
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

;; take object
(:action take
  :parameters (?v - robot ?o - obj ?p - person ?loc - waypoint)
  :precondition (and )
  :effect (and )
)

;; give object
(:action give
  :parameters (?v - robot ?o - obj ?p - person ?loc - waypoint)
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