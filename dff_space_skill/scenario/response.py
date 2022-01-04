import random
import re
from df_engine.core import Actor, Context
from scenario.condition import PLANET_COMPILED_PATTERN
import json
import os

FACT_LIST = dict()
PLANET = "mars"

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'data'))
wiki_json = os.path.join(data_dir,'planets_wiki.json')
with open(wiki_json) as inf:
    wiki_data = json.load(inf)

for planet,summary in wiki_data.items():
    FACT_LIST[planet] = [sentence + '.' for sentence in summary.split('.')]

def random_planet_fact(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    global PLANET
    request = ctx.last_request
    try:
        PLANET = PLANET_COMPILED_PATTERN.findall(request)[0].lower()
        fact = random.sample(FACT_LIST[PLANET], 1)[0]
        question = f"Would you like to hear another fun fact about {PLANET}?"
        return f"{fact}\n{question}"
    except IndexError:
        pass
        
def repeat_fact(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    global PLANET
    try:
        fact = random.sample(FACT_LIST[PLANET], 1)[0]
        question = f"Would you like to hear another fun fact about {PLANET}?"
        return f"{fact}\n{question}"
    except IndexError:
        pass