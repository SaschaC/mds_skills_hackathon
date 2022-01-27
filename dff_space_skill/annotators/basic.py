import re

from df_engine.core import Context

yes_regexp = re.compile(r"(\b|^)(yes|ja\b)(\b|$)",re.I)


def yes_intent(ctx: Context):
    ctx.misc["yes_intent"] = bool(yes_regexp.search(ctx.last_request))
    return ctx


no_regexp = re.compile(r"(\b|^)(no|nein)(\b|$)",re.I)


def no_intent(ctx: Context):
    ctx.misc["no_intent"] = bool(no_regexp.search(ctx.last_request))  # сохранение интента в контекст
    return ctx
