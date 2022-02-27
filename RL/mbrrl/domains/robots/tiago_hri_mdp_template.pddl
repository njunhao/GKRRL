(define (domain tiago_hri_mdp)
(:requirements :strips :typing ) ;;probabilistic-effects  )
(:types waypoint robot obj person)
(:predicates
  ; (TASK_REWARD)
  ; (COST)
  ; (PROB_LOSING_LOCALISATION ?v - robot)
  (robot_at ?v - robot ?loc - waypoint)
  (localised ?v - robot)
  (emptyhand ?v - robot)
  (holding ?v - robot ?o - obj)
  (object_at ?o - obj ?loc - waypoint)
  (object_with ?o - obj ?p - person)
  (goal_object_at ?o - obj ?loc - waypoint)
  (goal_object_with ?o - obj ?p - person)
  (person_at ?p - person ?loc - waypoint)
  (need_assistance ?p - person)
  (needed_assistance ?p - person) 
  (goal_attempted ?o - obj)
  (reward_received ?o - obj)
  (PROB_NEED_ASSISTANCE ?p - person)
  (TABLE_AT ?loc - waypoint)
  (PERSON_GOAL_OBJECT_AT ?p - person ?o - obj ?loc - waypoint)
  (PERSON_GOAL_OBJECT_WITH ?p - person ?o - obj ?p - person)
  (PERSON_IS_AT ?p - person ?loc - waypoint)
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

;; find person
(:action find_person
  :parameters (?v - robot ?p - person)
  :precondition (and )
  :effect (and )
)

;; talk
(:action talk_to_person
  :parameters (?v - robot ?p - person)
  :precondition (and )
  :effect (and )
)


;; pick up object
(:action pick_up
  :parameters (?v - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

;; put down object
(:action put_down
  :parameters (?v - robot ?o - obj)
  :precondition (and )
  :effect (and )
)

;; take from
(:action take
  :parameters (?v - robot ?o - obj ?p - person)
  :precondition (and )
  :effect (and )
)

;; give to
(:action give
  :parameters (?v - robot ?o - obj ?p - person)
  :precondition (and )
  :effect (and )
)

)