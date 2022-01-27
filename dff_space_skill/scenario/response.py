import re
from df_engine.core import Actor, Context
from langcodes import normalize_characters
from torch import norm, normal
from scenario.qcfg import g 
from nltk import grammar, parse
import re
from lxml import etree
import urllib.request, gzip, io
import scenario.config as config

def find_planets(query,gram):
    # remove numbers from query and substitute by '#NUM#'
    #print(f'Orig NL Query: {query}')
    query,number_dict = serialize(query)
    query = normalize(query)
    normalized_query = (f'Normalized NL Query: {query}')
    # parse query
    parser = parse.FeatureEarleyChartParser(gram)
    try:
        trees = list(parser.parse(query.split()))
    except ValueError:
        return('QueryError',0,0,0)
    if not trees:
        return('QueryError',0,0,0)
    for i,t in enumerate(trees):
        answer = trees[i].label()['SEM']
        language = trees[i].label()['L']
        answer = ''.join([s for s in answer if s])
        # substitute back in the numbers:
        for tag in number_dict.keys():
            answer = re.sub(tag,number_dict[tag],answer)
        subqueries = answer.split(';')
        planet_names = []
        if are_wellformed(subqueries):
            
            found = False
            try:
                for q in subqueries:
                    planets = oec.xpath(q)
                    if planets:
                        found = True
                    planet_names.append(get_names(planets))
                xml_queries=f'XML Queries:{subqueries}'
                if found:
                    return (planet_names,language,normalized_query,xml_queries)
                else:
                    continue
            except:
                continue
    if not planet_names:
        return ('QueryError',0,0,0)
    else:
        return (planet_names,language,normalized_query,xml_queries)

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
        response = give_de_response(planet_names,query)
    else:
        response = give_en_response(planet_names,query)
    return response

def give_en_response(planet_names,query):
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            config.PLANET_FOUND = True
            return f"I found the following {len(planet_names[0])} planet for the query '{query}':\n\n{', '.join(planet_names[0])}\n"
        elif len(planet_names[0]) > 1:
            config.PLANET_FOUND = True
            return f"I found the following {len(planet_names[0])} planets for the query '{query}':\n\n{', '.join(planet_names[0])}\n"
            
        else:
            return f"I did not find any planet for the query '{query}'.\n"   
    elif len(planet_names) > 1:
        response = ""
        for sqi,names in enumerate(planet_names):
            if len(names) == 1:
                config.PLANET_FOUND = True
                response += f"Here is 1 planet I found for part {sqi + 1} of the query '{query}':\n\n{names[0]}\n\n"
                
            elif len(names) > 1:
                config.PLANET_FOUND = True
                response += f"Here are {len(names)} planets I found for part {sqi + 1} of the query '{query}':\n\n{', '.join(names)}\n\n"
                
            else:
                response += f"I did not find any planet for part {sqi + 1} of the query '{query}'.\n\n"
        return response

def give_de_response(planet_names,query):
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            config.PLANET_FOUND = True
            return f"Ich habe den folgenden Planeten gefunden für die Anfrage '{query}':\n\n{', '.join(planet_names[0])}\n"
        elif len(planet_names[0]) > 1:
            config.PLANET_FOUND = True
            return f"Ich habe die folgenden {len(planet_names[0])} Planeten gefunden für die Anfrage '{query}:'\n\n{', '.join(planet_names[0])}\n"
        else:
            return f"Ich habe keine Planeten gefunden für die Anfrage '{query}'\n"
    elif len(planet_names) > 1:
        response = ""
        for sqi,names in enumerate(planet_names):
            if len(names) == 1:
                config.PLANET_FOUND = True
                response += f"Hier ist 1 Planet, den ich für Teil {sqi + 1} der Anfrage '{query}' gefunden habe:\n\n{names[0]}\n\n"
            elif len(names) > 1:
                config.PLANET_FOUND = True
                response += f"Hier sind {len(names)} Planeten, die ich für Teil {sqi + 1} der Anfrage '{query}' gefunden habe:\n\n{', '.join(names)}\n\n"
                
            else: 
                response += f"Ich habe keine Planeten für Teil {sqi + 1} der Anfrage '{query}' gefunden.\n\n"
        return response

gram = grammar.FeatureGrammar.fromstring(g)
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

speech_acts = {'another_search':{'de':'Möchtest du eine neue Suche starten?','en':'Would you like to try another search?'},
'no_understand':{'de':'Ich habe die diese Anfrage nicht verstanden:','en':'I did not understand the query'},
'spelling':{'de':'Entschuldige, bitte achte auf korrekte Rechtschreibung. Drücke eine Taste, um es erneut zu versuchen.','en':'Sorry, please spell correctly. Press any key to try again.'},
'more_info':{'de':'Möchtest du mehr über einen dieser Planeten erfahren?','en':'Would you like more info on one of these planets?'},
'initiate':{'de':'Bitte gib deine Anfrage ein.','en':'Please enter your search query!'},
'follow_up':{'de':'OK, über welchen Planeten?','en':'Alright, for which planet?'},
'fail':{'de':'Oh, hier ist etwas schief gelaufen. Drücke eine Taste, um von Vorne zu beginnen.','en':'Oh, something went wrong. Press any key to start from the beginning.'}}

def fail(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['fail'][config.LANGUAGE]

def initiate(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['initiate'][config.LANGUAGE]

def follow_up(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['follow_up'][config.LANGUAGE]

def another_search(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['another_search'][config.LANGUAGE]

def process_query(ctx: Context, actor: Actor, *args, **kwargs):
    config.PLANET_FOUND = False
    query = ctx.last_request
    planet_names,language,normalized_query,xml_queries = find_planets(query,gram)
    if language:
        config.LANGUAGE = language
    if planet_names == 'QueryError':
        response = speech_acts['no_understand'][config.LANGUAGE]
        question = question = speech_acts['another_search'][config.LANGUAGE]
        return f"\n\n{normalized_query}\n{xml_queries}\n\n{response} '{query}'. {question}\n"
    else:
        response = give_response(planet_names,query,language)
        if config.PLANET_FOUND:
            question = speech_acts['more_info'][config.LANGUAGE]
        else:
            question = speech_acts['another_search'][config.LANGUAGE]
        return f'\n\n{normalized_query}\n{xml_queries}\n\n{response}\n{question}\n'

def planet_description(ctx: Context, actor: Actor, *args, **kwargs):
    planet = ctx.last_request
    try:
        description = oec.xpath(f'.//planet[name="{planet}"]/description')[0].text
        config.SPELLING_CORRECT = True
        question = speech_acts['another_search'][config.LANGUAGE]
        return f'\n\n{description}\n\n{question}\n'
    except:
        config.SPELLING_CORRECT = False
        response = speech_acts['spelling'][config.LANGUAGE]
        return response