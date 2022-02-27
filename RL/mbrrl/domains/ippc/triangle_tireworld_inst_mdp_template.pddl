(define (problem rpg)
  (:domain triangle)
  (:objects la1a1 la1a2 la1a3 la1a4 la1a5 la1a6 la1a7 la1a8 la1a9 la1a10 la1a11 la2a1 la2a2 la2a3 la2a4 la2a5 la2a6 la2a7 la2a8 la2a9 la2a10 la3a1 la3a2 la3a3 la3a4 la3a5 la3a6 la3a7 la3a8 la3a9 la4a1 la4a2 la4a3 la4a4 la4a5 la4a6 la4a7 la4a8 la5a1 la5a2 la5a3 la5a4 la5a5 la5a6 la5a7 la6a1 la6a2 la6a3 la6a4 la6a5 la6a6 la7a1 la7a2 la7a3 la7a4 la7a5 la8a1 la8a2 la8a3 la8a4 la9a1 la9a2 la9a3 la10a1 la10a2 la11a1 - location) 
  (:init
    (not-flattire)
    (hasspare)
    (vehicle-at la1a1)
    (spare-in la2a1)
    (road la1a1 la1a2)
    (goal-reward-received)
    (goal-location la1a11)
  )
  (:constants
    (road la1a1 la1a2)
    (goal-location la1a11)
  )
          
  (:goal (and
    (vehicle-at la1a11)
  ))
  ; (:goal-reward 1)
  ; (:metric maximize (reward))
)
