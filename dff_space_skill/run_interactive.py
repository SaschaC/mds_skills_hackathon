#!/usr/bin/env python

import time
from typing import Optional, Union

from scenario.main import actor
from df_engine.core import Actor, Context
from annotators.main import annotate

def turn_handler(
    in_request: str,
    ctx: Union[Context, str, dict],
    actor: Actor,
    true_out_response: Optional[str] = None,
):
    # Context.cast - gets an object type of [Context, str, dict] returns an object type of Context
    ctx = Context.cast(ctx)

    # Add in current context a next request of user
    ctx.add_request(in_request)
    ctx = annotate(ctx)

    # pass the context into actor and it returns updated context with actor response
    ctx = actor(ctx)
    # get last actor response from the context
    out_response = ctx.last_response
    # the next condition branching needs for testing
    if true_out_response is not None and true_out_response != out_response:
        raise Exception(f"{in_request} -> true_out_response != out_response: {true_out_response} != {out_response}")
    else:
        print(f"{in_request} -> {out_response}")
    return out_response, ctx

if __name__ == "__main__":
    ctx = {}
    input("""\nHi, I help you search for exoplanets. 
You can ask me things in English and German. For example, 'Which planets that were discovered before 2010 have a radius of at least 3 and a mass of at most 4', 
'Show me 5 planets with a mass smaller than 2 and 3 planets that were discovered before 2010', 'Welche Planeten, die vor 2010 entdeckt wurden, haben einen Radius von 
mindestens 3 und eine Masse von maximal 4', 'Zeig mir 5 Planeten mit einer Masser von maximal 2 und 3 Planeten, die vor 2010 entdeckt wurden.'
The parameters that I understand are radius (de: 'radius'), mass (de: 'Masse'), age (de: 'Alter'), and discovered (de: 'entdeckt'). For more info on what the parameters mean visit:
https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/

Press an key to get started.

""")
    while True:
        in_request = input("\nType your answer: ")
        st_time = time.time()
        out_response, ctx = turn_handler(in_request, ctx, actor)
        total_time = time.time() - st_time
        print(f"exec time = {total_time:.3f}s")