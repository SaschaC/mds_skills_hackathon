import df_engine.conditions as cnd
from df_engine.core import Actor
from df_engine.core.keywords import LOCAL, RESPONSE, TRANSITIONS
import re
import scenario.condition as loc_cnd
import scenario.response as rsp
import df_engine.labels as lbl

plot = {
    "service": {
        LOCAL: {
            TRANSITIONS: {
                ("planets", "node1"): cnd.true(),
            }
        },
        "start": {RESPONSE: ""},
        "fallback": {RESPONSE: "Sorry"},
    },
    "planets": {
        "node1": {
            RESPONSE: "Which planet would you like to know about?",
            TRANSITIONS: {
                "node2": loc_cnd.planet_condition}
            },
        "node2": {
            RESPONSE: rsp.random_planet_fact,
            TRANSITIONS: {
                "node3": loc_cnd.another_funfact_condition,"node1":loc_cnd.different_funfact_condition}
        },
        "node3": {
            RESPONSE: rsp.repeat_fact,
            TRANSITIONS: {
                "node3": loc_cnd.another_funfact_condition,"node1":loc_cnd.different_funfact_condition}
        },
    }
}

actor = Actor(plot, start_label=("service", "start"), fallback_label=("service", "fallback"))