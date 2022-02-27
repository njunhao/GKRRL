(define (domain triangle)
  (:requirements :strips :typing ) ;;probabilistic-effects  )
  (:types location)
  (:predicates 
    (vehicle-at ?loc - location)
    (spare-in ?loc - location)
    (road ?from - location ?to - location)
    (not-flattire)
    (hasspare)
    (goal-location ?loc - location)
    (goal-reward-received)
  )
  
  (:action move-car
    :parameters (?from - location ?to - location)
    :precondition (and )
    :effect (and )
  )

  (:action loadtire
    :parameters (?loc - location)
    :precondition (and )
    :effect (and )
  )

  (:action changetire
    :precondition (and )
    :effect (and )
  )

)