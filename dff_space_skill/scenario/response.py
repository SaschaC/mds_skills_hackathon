import random
import re
from df_engine.core import Actor, Context
from scenario.condition import PLANET_COMPILED_PATTERN
from scenario.qcfg import g 
import json
import os
from nltk import grammar, parse
import nltk,urllib.request, gzip, io
from nltk import grammar, parse
import re
from lxml import etree

FACT_LIST = dict()
PLANET = "mars"

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,'data'))
wiki_json = os.path.join(data_dir,'planets_wiki.json')
with open(wiki_json) as inf:
    wiki_data = json.load(inf)

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
gram = grammar.FeatureGrammar.fromstring(g)

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


def find_planets(query,gram):
    # remove numbers from query and substitute by '#NUM#'
    print(f'Orig NL Query: {query}')
    query,number_dict = serialize(query)
    query = normalize(query)
    print(f'Normalized NL Query: {query}')
    # parse query
    parser = parse.FeatureEarleyChartParser(gram)
    try:
        trees = list(parser.parse(query.split()))
    except ValueError:
        return('You used some words I do not understand.')

    for i,t in enumerate(trees):
        answer = trees[i].label()['SEM']
        language = trees[i].label()['L']
        answer = ''.join([s for s in answer if s])
        # substitute back in the numbers:
        for tag in number_dict.keys():
            answer = re.sub(tag,number_dict[tag],answer)
        subqueries = answer.split(';')
        if are_wellformed(subqueries):
            planet_names = []
            try:
                for q in subqueries:
                    planets = oec.xpath(q)
                    planet_names.append(get_names(planets))
                print('XML Queries: ',subqueries)
                print(f'Tree number: {i}')
                return (planet_names,language)
            except:
                continue
    return 'XPathEvalError'

def serialize(query):
    number_dict = dict()
    numbers = re.findall(r'(\d+\.*\d*)',query)
    number_tags = ['#NUM'+str(i) for i in range(len(numbers))]
    for i,tag in enumerate(number_tags):
        number_dict[tag] = numbers[0]
        query = re.sub(f'(?<!NUM)({numbers[0]})',tag,query,count=1)
        numbers = re.findall(r'(?<!NUM)(\d+\.*\d*)',query)
    return (query,number_dict)

def normalize(query):
    query = query.lower()
    query = re.sub(r'[^\w\s#]','',query)
    query = re.sub(
        r'zeig mir|show me|are there any|are there|gibt es|can you show me|look for|search|suche?|finde?',
        '',query)
    return query
    
def are_wellformed(qs):
    wf = re.compile('\.//.+?\[.+?\]|\(\.//.+?\[.+?\]\)\[.+?\]')
    for q in qs:
        if not wf.match(q):
            return 0
    return 1

def get_names(elements):
    names = []
    for e in elements:
        names.append(e.xpath("name")[0].text)
    return names

def give_response(planet_names,query,language):
    if language == 'de':
        give_de_response(planet_names,query)
    else:
        give_en_response(planet_names,query)

def give_en_response(planet_names,query):
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            return(
            f"I found the following {len(planet_names[0])} planet for the query '{query}:'\n{', '.join(planet_names[0])}\n"
            )
        elif len(planet_names[0]) > 1:
            return(
            f"I found the following {len(planet_names[0])} planet(s) for the query '{query}:'\n{', '.join(planet_names[0])}\n"
            )
        else:
            return(f"I did not find any planet for the query '{query}'.\n"
            )
    elif len(planet_names) > 1:
        for sqi,names in enumerate(planet_names):
            if len(names) == 1:
                return(
                f"Here is 1 planet I found for part {sqi} of the query '{query}:'\n{names[0]}\n"
                )
            elif len(names) > 1:
                return(
                f"Here are {len(names)} planets I found for part {sqi} of the query '{query}':\n{', '.join(names)}\n"
                )
            else:
                return(f"I did not find any planet for part {sqi} of the query '{query}'.\n"
                )

def give_de_response(planet_names,query):
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            return(
            f"Ich habe den folgenden Planeten gefunden für die Anfrage '{query}'\n:{', '.join(planet_names[0])}\n"
            )    
        elif len(planet_names[0]) > 1:
            return(
            f"Ich habe die folgenden {len(planet_names[0])} Planeten gefunden für die Anfrage '{query}'\n:{', '.join(planet_names[0])}\n"
            )
        else:
            return(f"Ich habe keine Planeten gefunden für die Anfrage '{query}'\n"
            )
    elif len(planet_names) > 1:
        for sqi,names in enumerate(planet_names):
            if len(names) == 1:
                return(
                f"Hier ist 1 Planet, den ich für Teil {sqi} der Anfrage '{query}' gefunden habe:\n{names[0]}\n"
                )
            elif len(names) > 1:
                return(
                f"Hier sind {len(names)} Planeten, die ich für Teil {sqi} der Anfrage '{query}' gefunden habe:\n{', '.join(names)}\n"
                )
            else:
                return(f"Ich habe keine Planeten für Teil {sqi} der Anfrage '{query}' gefunden.\n"
                )
def process_query(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    QUERY = ctx.last_request
    planet_names,language = find_planets(QUERY[0],gram)
    if planet_names == 'XPathEvalError':
        return(f"I did not understand the query '{QUERY}'.\n")
    else:
        return give_response(planet_names,QUERY[0],language)