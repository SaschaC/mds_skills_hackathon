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

# Create the CFG grammar from a string saved in qcfg.py
gram = grammar.FeatureGrammar.fromstring(g)
# Get the expoplanet data and parse it into an XML tree
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
# Predefined response templates in German and English:
speech_acts = {'another_search':{'de':'Möchtest du eine neue Suche starten?','en':'Would you like to try another search?'},
'no_understand':{'de':'Ich habe die diese Anfrage nicht verstanden:','en':'I did not understand the query'},
'spelling':{'de':'Entschuldige, bitte achte auf korrekte Rechtschreibung. Drücke eine Taste, um es erneut zu versuchen.','en':'Sorry, please spell correctly. Press any key to try again.'},
'more_info':{'de':'Möchtest du mehr über einen dieser Planeten erfahren?','en':'Would you like more info on one of these planets?'},
'initiate':{'de':'Bitte gib deine Anfrage ein.','en':'Please enter your search query!'},
'follow_up':{'de':'OK, über welchen Planeten?','en':'Alright, for which planet?'},
'fail':{'de':'Oh, hier ist etwas schief gelaufen. Drücke eine Taste, um von Vorne zu beginnen.','en':'Oh, something went wrong. Press any key to start from the beginning.'},
'not_found':{'de':'Ich habe keine Planeten gefunden für die Anfrage ','en':'I did not find any planet for the query '}}

def find_planets(query,gram):
    '''
    Process the query and parse it with the CFG grammar. 
    If the query cannot be parsed the parser returns a ValueError or is empty 
    and the function will return an error. If the query can be parsed all created parse trees are iterated over
    and their 'SEM' feature holding the created Xpath query is extracted. It is then verified that
    this Xpath query is well-formed (e.g., '../planet[radius=1]'), and if it is, then the XML expoplanet database is queried.
    INPUT: 
    - query: string; the original input query, e.g., 'planets with a radius of 1'
    - gram: NLTK FeatureGrammar object created from grammar defined in qcfg.py
    OUTPUT: tuple:
    - planet_names: list of lists; if the length of the outer list is 1, the query had 1 part, e.g. 'planet with a radius of 1';
      if the length of the outer list is > 1, the query had multiple parts, e.g. 
      '2 planets with a radius of 1 and 1 planet with a mass of 1'
    - language; either 'de' or 'en'; this is the CFG tree feature 'L'
    - normalized_query; query processed with normalize() and serialize()
    - xml_queries: the queries in Xpath format
    '''
    # remove numbers from query and substitute by '#NUM#'
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
    planet_names = []
    for i,t in enumerate(trees):
        answer = trees[i].label()['SEM']
        language = trees[i].label()['L']
        # join the parts of the featue 'SEM' into one continous string:
        answer = ''.join([s for s in answer if s])
        # substitute back in the numbers:
        for tag in number_dict.keys():
            answer = re.sub(tag,number_dict[tag],answer)
        subqueries = answer.split(';')
        if are_wellformed(subqueries):
            planet_names = []
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
    return (0,language,normalized_query,xml_queries)

def serialize(query):
    '''
    Replace the numbers in the query with numbered tags, 
    e.g., 'planets with a radius of 1' -> 'planets with a radius of #NUM0'.
    Create a dictionary in order to later reassign the numbers to the tags.
    INPUT: query; the original query
    OUTPUT: 
    - query with replaced numbers, e.g., 'planets with a radius of #NUM0'
    - number_dict: dictionary with number tags as keys (e.g., #NUM0) 
      and numbers as values (e.g., 1)
    '''
    number_dict = dict()
    numbers = re.findall(r'(\d+\.*\d*)',query)
    number_tags = ['#NUM'+str(i) for i in range(len(numbers))]
    for i,tag in enumerate(number_tags):
        number_dict[tag] = numbers[0]
        query = re.sub(f'(?<!NUM)({numbers[0]})',tag,query,count=1)
        numbers = re.findall(r'(?<!NUM)(\d+\.*\d*)',query)
    return (query,number_dict)

def normalize(query):
    '''
    Normalize the input query and remove redundant material 
    that is not relevant for the parsing of the query.
    '''
    query = query.lower()
    query = re.sub(r'[^\w\s#]','',query)
    query = re.sub(
        r'zeig mir|show me|are there any|are there|gibt es|can you show me|look for|search|suche?|finde?',
        '',query)
    return query
    
def are_wellformed(qs):
    '''
    Check if the given queries are in a well-formed Xpath format.
    RETURN: true if all queries are well-formed, false otherwise 
    '''
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
    '''
    Provide search result response in case the search yielded planets. 
    The language has been extracted from the parsed and processed query 
    and determines the language of the response. 
    INPUT:
    - planet_names: list of lists; if the length of the outer list is 1, the query had 1 part, e.g. 'planet with a radius of 1';
      if the length of the outer list is > 1, the query had multiple parts, e.g. 
      '2 planets with a radius of 1 and 1 planet with a mass of 1'
    - query: string; the original input query
    - language: string
    OUTPUT: string built from the planet names embedded in language-specific response templates.
    '''
    if language == 'de':
        response = give_de_response(planet_names,query)
    else:
        response = give_en_response(planet_names,query)
    return response

def give_en_response(planet_names,query):
    '''
    See calling function give_response()
    '''
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            return f"I found the following {len(planet_names[0])} planet for the query '{query}':\n\n{', '.join(planet_names[0])}\n"
        elif len(planet_names[0]) > 1:
            return f"I found the following {len(planet_names[0])} planets for the query '{query}':\n\n{', '.join(planet_names[0])}\n"   
    elif len(planet_names) > 1:
        response = ""
        for sqi,names in enumerate(planet_names):
            if len(names) == 1:
                response += f"Here is 1 planet I found for part {sqi + 1} of the query '{query}':\n\n{names[0]}\n\n"                
            elif len(names) > 1:
                response += f"Here are {len(names)} planets I found for part {sqi + 1} of the query '{query}':\n\n{', '.join(names)}\n\n"
            else: 
                response += f"I did not find any planet for part {sqi + 1} of the query '{query}'.\n\n"
        return response

def give_de_response(planet_names,query):
    '''
    See calling function give_response()
    '''
    if len(planet_names) == 1:
        if len(planet_names[0]) == 1:
            config.PLANET_FOUND = True
            return f"Ich habe den folgenden Planeten gefunden für die Anfrage '{query}':\n\n{', '.join(planet_names[0])}\n"
        elif len(planet_names[0]) > 1:
            config.PLANET_FOUND = True
            return f"Ich habe die folgenden {len(planet_names[0])} Planeten gefunden für die Anfrage '{query}:'\n\n{', '.join(planet_names[0])}\n"
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

def process_query(ctx: Context, actor: Actor, *args, **kwargs):
    '''
    Initiate the processing of the input query and return a presentation of the search result.
    The processing and parsing of the input query is done within find_planets(). The language is extracted
    from the parsed query and used to set the language of the response. 
    OUTPUT: String containing:
     - normalized_query: numbers replaced by placeholders that are recognized by the CFG grammar,
        lower-cased, punctuation removed
     - xml_queries: the converted query in Xpath format.
     - response: the presentation of the search result including
     - question: follow-up question for the user 
    '''
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
        if planet_names:
            config.PLANET_FOUND = True
            response = give_response(planet_names,query,language)
            question = speech_acts['more_info'][config.LANGUAGE]
            return f'\n\n{normalized_query}\n{xml_queries}\n\n{response}\n{question}\n'

        else:
            config.PLANET_FOUND = False
            response = speech_acts['not_found'][config.LANGUAGE]
            question = speech_acts['another_search'][config.LANGUAGE]
            return f"\n\n{normalized_query}\n{xml_queries}\n\n{response}'{query}'\n\n{question}\n"

def planet_description(ctx: Context, actor: Actor, *args, **kwargs):
    '''
    Retrieve a description from the data base via Xpath for the planet provided by the user.
    OUTPUT: String with description or prompt to provide the correctly spelled name of a planet. 
    '''
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

def fail(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['fail'][config.LANGUAGE]

def initiate(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['initiate'][config.LANGUAGE]

def follow_up(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['follow_up'][config.LANGUAGE]

def another_search(ctx: Context, actor: Actor, *args, **kwargs):
    return speech_acts['another_search'][config.LANGUAGE]