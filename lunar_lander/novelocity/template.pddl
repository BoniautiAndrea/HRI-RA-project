;problem file of lunar lander domain
(define (problem problem_1)
    (:domain lunar_lander_novel)
    (:init 
        ;current initial position, modify only the first line of predicates unless having modified the size of the domain
        (current_t t_0) (current_x x_0) (current_y y_0)
        ;predicates needed to construct and connect the discrete domain
        ;limit cases included in next and prev predicates to allow limit cases in actions parameters
        (next t_-3 t_-4) (next t_-2 t_-3) (next t_-1 t_-2) (next t_0 t_-1) (next t_1 t_0) (next t_2 t_1) (next t_3 t_2) (next t_4 t_3) (next t_4 t_4) 
        (next x_-9 x_-10) (next x_-8 x_-9) (next x_-7 x_-8) (next x_-6 x_-7) (next x_-5 x_-6) (next x_-4 x_-5) (next x_-3 x_-4) (next x_-2 x_-3) (next x_-1 x_-2) (next x_0 x_-1) (next x_1 x_0) (next x_2 x_1) (next x_3 x_2) (next x_4 x_3) (next x_5 x_4) (next x_6 x_5) (next x_7 x_6) (next x_8 x_7) (next x_9 x_8) (next x_10 x_9) (next x_10 x_10)
        (next y_0 y_-1) (next y_1 y_0) (next y_2 y_1) (next y_3 y_2) (next y_4 y_3) (next y_5 y_4) (next y_6 y_5) (next y_7 y_6) (next y_8 y_7) (next y_9 y_8) (next y_10 y_9) (next y_10 y_10) ;(next y_-9 y_-10) (next y_-8 y_-9) (next y_-7 y_-8) (next y_-6 y_-7) (next y_-5 y_-6) (next y_-4 y_-5) (next y_-3 y_-4) (next y_-2 y_-3) (next y_-1 y_-2)
        (prev t_-4 t_-4) (prev t_-4 t_-3) (prev t_-3 t_-2) (prev t_-2 t_-1) (prev t_-1 t_0) (prev t_0 t_1) (prev t_1 t_2) (prev t_2 t_3) (prev t_3 t_4)  
        (prev x_-10 x_-10) (prev x_-10 x_-9) (prev x_-9 x_-8) (prev x_-8 x_-7) (prev x_-7 x_-6) (prev x_-6 x_-5) (prev x_-5 x_-4) (prev x_-4 x_-3) (prev x_-3 x_-2) (prev x_-2 x_-1) (prev x_-1 x_0) (prev x_0 x_1) (prev x_1 x_2) (prev x_2 x_3) (prev x_3 x_4) (prev x_4 x_5) (prev x_5 x_6) (prev x_6 x_7) (prev x_7 x_8) (prev x_8 x_9) (prev x_9 x_10) 
        (prev y_-1 y_-1) (prev y_-1 y_0) (prev y_0 y_1) (prev y_1 y_2) (prev y_2 y_3) (prev y_3 y_4) (prev y_4 y_5) (prev y_5 y_6) (prev y_6 y_7) (prev y_7 y_8) (prev y_8 y_9) (prev y_9 y_10) ;(prev y_-10 y_-10) (prev y_-10 y_-9) (prev y_-9 y_-8) (prev y_-8 y_-7) (prev y_-7 y_-6) (prev y_-6 y_-5) (prev y_-5 y_-4) (prev y_-4 y_-3) (prev y_-3 y_-2) (prev y_-2 y_-1) 
    )

    (:goal (and 
        (current_y y_0) (current_t t_0) (current_x x_0)
        )
    )
)