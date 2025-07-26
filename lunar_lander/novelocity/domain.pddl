(define (domain lunar_lander_novel)

(:requirements :typing :conditional-effects :negative-preconditions :equality :non-deterministic)

(:types
    value
    x_value y_value t_value - value
)

(:constants
    t_-1 t_-2 t_-3 t_-4 t_0 t_1 t_2 t_3 t_4 - t_value
    x_-1 x_-2 x_-3 x_-4 x_-5 x_-6 x_-7 x_-8 x_-9 x_-10 x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 x_8 x_9 x_10 - x_value 
    y_-1 y_0 y_1 y_2 y_3 y_4 y_5 y_6 y_7 y_8 y_9 y_10 - y_value
)

(:predicates
    (current_x ?x - x_value)
    (current_y ?y - y_value)
    (current_t ?t - t_value)
    (next ?n ?v - value)
    (prev ?p ?v - value)
)

(:action idle
        :parameters (?y_prev ?y - y_value)
        :precondition (and 
            (current_y ?y) (not(current_y y_0))
            (prev ?y_prev ?y)
        )
        :effect (and
            (oneof (and (not (current_y ?y)) (current_y ?y_prev)) (and))
        )
    )

(:action main_engine
        :parameters (?y ?y_next - y_value)
        :precondition (and 
            (current_y ?y) (not(current_y y_0))
            (next ?y_next ?y)
        )
        :effect (and
            (oneof (and (not (current_y ?y)) (current_y ?y_next)) (and))
        )
    )

(:action right_engine
        :parameters (?x ?x_next - x_value
                     ?t_prev ?t - t_value)
        :precondition (and 
            (current_x ?x) (current_t ?t) (not(current_y y_0))
            (next ?x_next ?x)
            (prev ?t_prev ?t)
        )
        :effect (and
            (oneof (and (not (current_x ?x)) (current_x ?x_next)) (and))
            (oneof (and (not (current_t ?t)) (current_t ?t_prev)) (and))
        )
    )

(:action left_engine
        :parameters (?x_prev ?x - x_value
                     ?t ?t_next - t_value)
        :precondition (and 
            (current_x ?x) (current_t ?t) (not(current_y y_0))
            (prev ?x_prev ?x)
            (next ?t_next ?t)
        )
        :effect (and
            (oneof (and (not (current_x ?x)) (current_x ?x_prev)) (and))
            (oneof (and (not (current_t ?t)) (current_t ?t_next)) (and))
        )
    )

)