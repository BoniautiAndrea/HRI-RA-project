;lunar lander dicrete domain
;for solver reasons and limits it is not a numerical domain, the domain size is defined by constant values
;the non-determinism is induces by the discretization of the original domain, each constant is not just a
;singular value, but it represents an interval of the original continuous domain, except for 0 values
;ex. x_10 = (9,10]
(define (domain lunar_lander_simplified)
    (:requirements :typing :conditional-effects :negative-preconditions :equality :non-deterministic)

    ;types used to reduce variable choices in predicates and to have a better understandable code
    (:types 
        value
        t_value vt_value vx_value vy_value x_value y_value - value
    )

    ;needed constants to define the discrete domain
    (:constants t_-1 t_-2 t_0 t_1 t_2 - t_value
        vt_-1 vt_-2 vt_0 vt_1 vt_2 - vt_value
        vx_-1 vx_-2 vx_0 vx_1 vx_2 - vx_value
        vy_-1 vy_-2 vy_0 vy_1 - vy_value 
        x_-1 x_-2 x_-3 x_0 x_1 x_2 x_3 - x_value 
        y_-1 y_0 y_1 y_2 y_3 - y_value
    )

    (:predicates   
        ;current state definition x,y = cartesian position t(theta)=angle wrt x axis
        ;next and prev predicates used to connect domain values
        ;ex. from x_10 and x_9 -> (x_prev x_9 x_10) and (x_next x_10 x_9)
        (current_t ?t - t_value)  
        (current_vt ?vt - vt_value)  
        (current_vx ?vx - vx_value)  
        (current_vy ?vy - vy_value)  
        (current_x ?x - x_value)  
        (current_y ?y - y_value)
        ;predicates to define relations between constants
        (negative ?v - value)
        (next ?n ?v - value) 
        (positive ?v - value)  
        (prev ?p ?v - value)
    )

    ;Actions, to reduce computational time idle and main engine actions can just modify vertical motion
    ; and side engine actions can just modify horizontal and rotational motion

    ;idle action, no engine fired, the lander could just move in vertical direction, it actually can
    ;modify vertical velocity that then can induce the vertical motion
    (:action idle
        :parameters (?y_prev ?y ?y_next - y_value ?vy_prev ?vy - vy_value)
        :precondition (and 
            (current_y ?y) (current_vy ?vy) (not(current_y y_0))
            (prev ?y_prev ?y)
            (next ?y_next ?y)
            (prev ?vy_prev ?vy)
        )
        :effect (and
            (oneof (and (not (current_vy ?vy)) (current_vy ?vy_prev)) (and))
            (when 
                (positive ?vy) (oneof (and (not (current_y ?y)) (current_y ?y_next)) (and))
            )
            (when 
                (negative ?vy) (oneof (and (not (current_y ?y)) (current_y ?y_prev)) (and))
            )
        )
    )

    ;main engine motion, same logic as idle motion but inverse effect on vertical velocity
    (:action main_engine
        :parameters (?y_prev ?y ?y_next - y_value
                     ?vy ?vy_next - vy_value)
        :precondition (and 
            (current_y ?y) (current_vy ?vy) (not(current_y y_0))
            (prev ?y_prev ?y)
            (next ?y_next ?y)
            (next ?vy_next ?vy)
        )
        :effect (and
            (oneof (and (not (current_vy ?vy)) (current_vy ?vy_next)) (and))
            (when
                (positive ?vy) (oneof (and (not (current_y ?y)) (current_y ?y_next)) (and))
            )     
            (when
                (negative ?vy) (oneof (and (not (current_y ?y)) (current_y ?y_prev)) (and))
            )
        )
    )
    
    ;right engine action, can affect only horizontal and rotational velocity, then update x and t (theta)
    ;according to their sign respectively
    (:action right_engine
        :parameters (?x_prev ?x ?x_next - x_value
                     ?t_prev ?t ?t_next - t_value 
                     ?vx ?vx_next - vx_value
                     ?vt_prev ?vt - vt_value)
        :precondition (and 
            (current_x ?x) (current_t ?t) (current_vx ?vx) (current_vt ?vt) (not(current_y y_0))
            (prev ?x_prev ?x)
            (next ?x_next ?x)
            (prev ?t_prev ?t)
            (next ?t_next ?t)
            (next ?vx_next ?vx)
            (prev ?vt_prev ?vt)
        )
        :effect (and
            (oneof (and (not (current_vx ?vx)) (current_vx ?vx_next)) (and))
            (oneof (and (not (current_vt ?vt)) (current_vt ?vt_prev)) (and))
            (when
                (positive ?vx) (oneof (and (not (current_x ?x)) (current_x ?x_next)) (and))
            )
            (when
                (negative ?vx) (oneof (and (not (current_x ?x)) (current_x ?x_prev)) (and))
            )
            (when
                (positive ?vt) (oneof (and (not (current_t ?t)) (current_t ?t_next)) (and))
            )
            (when
                (negative ?vt) (oneof (and (not (current_t ?t)) (current_t ?t_prev)) (and))
            )
        )
    )
    
    ;same logic as right engine action, but inverse effects
    (:action left_engine
        :parameters (?x_prev ?x ?x_next - x_value
                     ?t_prev ?t ?t_next - t_value 
                     ?vx_prev ?vx - vx_value
                     ?vt ?vt_next - vt_value)
        :precondition (and 
            (current_x ?x) (current_t ?t) (current_vx ?vx) (current_vt ?vt) (not(current_y y_0)) 
            (prev ?x_prev ?x)
            (next ?x_next ?x)
            (prev ?t_prev ?t)
            (next ?t_next ?t)
            (prev ?vx_prev ?vx)
            (next ?vt_next ?vt)
        )
        :effect (and     
            (oneof (and (not (current_vx ?vx)) (current_vx ?vx_prev)) (and))
            (oneof (and (not (current_vt ?vt)) (current_vt ?vt_next)) (and))
            (when
                (positive ?vx) (oneof (and (not (current_x ?x)) (current_x ?x_next)) (and))
            )
            (when
                (negative ?vx) (oneof (and (not (current_x ?x)) (current_x ?x_prev)) (and))
            )
            (when
                (positive ?vt) (oneof (and (not (current_t ?t)) (current_t ?t_next)) (and))
            )
            (when
                (negative ?vt) (oneof (and (not (current_t ?t)) (current_t ?t_prev)) (and))
            )
        )
    )
)