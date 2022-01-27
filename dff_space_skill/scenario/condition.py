import logging
import re
from df_engine.core import Actor, Context
import scenario.config as config


logger = logging.getLogger(__name__)

def yes_intent_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get("yes_intent"))

def no_intent_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get("no_intent"))

def planet_found_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(config.PLANET_FOUND)

def planet_not_found_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(not config.PLANET_FOUND)

def spelling_correct_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(config.SPELLING_CORRECT)

def spelling_not_correct_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(not config.SPELLING_CORRECT)