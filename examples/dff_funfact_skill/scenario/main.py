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
                ("funfact", "random"): loc_cnd.random_funfact_condition,
            }
        },
        "start": {RESPONSE: ""},
        "fallback": {RESPONSE: "Sorry"},
    },
    "planets": {
        "node1": {
            RESPONSE: "Which planet would you like to know about?",
            TRANSITIONS: {
                lbl.forward: cnd.regexp(r'mars|venus|saturn',re.I)}
            },
        "node2": {
            RESPONSE: rsp.random_planet_fact,
            TRANSITIONS: {
                lbl.repeat: cnd.regexp(r'mars|venus|saturn',re.I)}
        },
    },
}

actor = Actor(plot, start_label=("service", "start"), fallback_label=("service", "fallback"))
