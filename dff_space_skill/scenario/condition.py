import logging
import re

from df_engine.core import Actor, Context


PLANET_COMPILED_PATTERN = re.compile(
    r"earth|venus|mars|mercury|jupiter|uranus|saturn|neptune",
    re.IGNORECASE,
)

logger = logging.getLogger(__name__)


def planet_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(PLANET_COMPILED_PATTERN.search(request))


def another_funfact_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(ctx.misc.get("yes_intent"))

def different_funfact_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(ctx.misc.get("no_intent"))