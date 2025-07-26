;problem file of lunar lander domain
(define (problem problem_1)
    (:domain mini_full)
    (:init 
        ;current initial position, modify only the first line of predicates unless having modified the size of the domain
        (current_x x_1) (current_y y_2) (current_t t_1) (current_vx vx_0) (current_vy vy_0) (current_vt vt_0) 
        ;predicates needed to construct and connect the discrete domain
        ;limit cases included in next and prev predicates to allow limit cases in actions parameters
        (negative vt_-1) 
        (negative vx_-1) 
        (negative vy_-1) (negative vy_-2)
        (next t_0 t_-1) (next t_1 t_0) (next t_1 t_1)
        (next vt_0 vt_-1) (next vt_1 vt_0) (next vt_1 vt_1)
        (next vx_0 vx_-1) (next vx_1 vx_0) (next vx_1 vx_1) 
        (next vy_-1 vy_-2) (next vy_0 vy_-1) (next vy_1 vy_0) (next vy_1 vy_1) 
        (next x_0 x_-1) (next x_1 x_0) (next x_1 x_1)
        (next y_1 y_0) (next y_2 y_1) (next y_2 y_2)
        (positive vt_1)
        (positive vx_1)
        (positive vy_1)
        (prev t_-1 t_-1) (prev t_-1 t_0) (prev t_0 t_1)
        (prev vt_-1 vt_-1) (prev vt_-1 vt_0) (prev vt_0 vt_1)
        (prev vx_-1 vx_-1) (prev vx_-1 vx_0) (prev vx_0 vx_1) 
        (prev vy_-2 vy_-2) (prev vy_-2 vy_-1) (prev vy_-1 vy_0) (prev vy_0 vy_1)
        (prev x_-1 x_-1) (prev x_-1 x_0) (prev x_0 x_1)
        (prev y_0 y_0) (prev y_0 y_1) (prev y_1 y_2)
    )

    (:goal (and 
        (current_y y_0) (current_t t_0) (current_x x_0) (current_vy vy_0)
        )
    )
)