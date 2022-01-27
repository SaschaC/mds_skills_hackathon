import df_engine.conditions as cnd
from df_engine.core import Actor
from df_engine.core.keywords import LOCAL, RESPONSE, TRANSITIONS
import scenario.condition as loc_cnd
import scenario.response as rsp
import df_engine.labels as lbl
from lxml import etree

plot = {
    "service": {
        LOCAL: {
            TRANSITIONS: {
                ("planets", "node1"): cnd.true(),
            }
        },
        "start": {RESPONSE: ""},
        "fallback": {RESPONSE: rsp.fail},
    },
    "planets": {
        "node1": {
            RESPONSE: rsp.initiate,
            TRANSITIONS: {
                "node2": cnd.true()}
            },
        "node2": {
            RESPONSE: rsp.process_query,
            TRANSITIONS: {
                "node3": cnd.all([loc_cnd.yes_intent_condition,loc_cnd.planet_found_condition]),
                "node5": cnd.all([loc_cnd.no_intent_condition, loc_cnd.planet_found_condition]),
                "node1":cnd.all([loc_cnd.yes_intent_condition, loc_cnd.planet_not_found_condition]),
                "node6":cnd.all([loc_cnd.no_intent_condition, loc_cnd.planet_not_found_condition])}
        },
        "node3": {
            RESPONSE: rsp.follow_up,
            TRANSITIONS: {
                "node4":cnd.true()}
        },
        "node4": {
            RESPONSE: rsp.planet_description,
            TRANSITIONS: {
                "node1":loc_cnd.spelling_correct_condition and loc_cnd.yes_intent_condition,
                "node6":loc_cnd.spelling_correct_condition and loc_cnd.no_intent_condition,
                "node3":loc_cnd.spelling_not_correct_condition}
        },
        "node5": {
            RESPONSE: rsp.another_search,
            TRANSITIONS: {
                "node1": loc_cnd.yes_intent_condition,"node6":loc_cnd.no_intent_condition}
        },
        "node6": {
            RESPONSE: "OK bye!",
            TRANSITIONS: {
                "node1": cnd.true()}
    }
}
}

actor = Actor(plot, start_label=("service", "start"), fallback_label=("service", "fallback"))