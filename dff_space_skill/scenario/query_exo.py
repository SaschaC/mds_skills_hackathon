
import nltk
from nltk import grammar, parse
from nltk.tokenize import word_tokenize
import re
import xml.etree.ElementTree as ET, urllib.request, gzip, io


def translate_query(query,g):
    # remove numbers from query and substitute by '#NUM#'
    numbers = re.findall(r'\d+\.*\d+',query)
    query = re.sub(r'\d+\.*\d+','#NUM#',query)
    gram = grammar.FeatureGrammar.fromstring(g)
    # parse query
    parser = parse.FeatureEarleyChartParser(gram)
    trees = list(parser.parse(query.split()))

    # get the query translated into XPath
    answer = trees[0].label()['SEM']
    answer = [s for s in answer if s]
    q_xpath = ''.join(answer)
    # substitute back in the numbers:
    for n in numbers:
        q_xpath = re.sub(r'#NUM#',n,q_xpath,count=1)
    print('\nQuery: ',q_xpath,'\n')
    return q_xpath


# grammar
g = """
% start S
S[SEM=(?np + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]
VP[SEM=(?v + ?np)] -> TV[SEM=?v] NP[SEM=?np]
NP[SEM=(?det + ?n)] -> Art[SEM=?det] NP[SEM=?n]
NP[SEM=(?int + ?n)] -> Int[SEM=?int] N[SEM=?n]
NP[SEM=(?np + ?pp)] -> NP[SEM=?np] PP[SEM=?pp]
PP[SEM=(?p + ?np)] -> P[SEM=?p] NUM[SEM=?np]
Int[SEM='.//'] -> 'which' | 'what'
TV[SEM=''] -> 'have'
Art[SEM=''] -> 'a'
NP[SEM='[mass'] -> 'mass'
NP[SEM='[radius'] -> 'radius'
N[SEM='planet'] -> 'planet' | 'planets'
P[SEM=''] -> 'of'
NUM[SEM="='#NUM#']"] -> '#NUM#'
"""
# get xml exoplanet database:
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

queries = ['what planets have a mass of 19.4','which planets have a mass of 19.4','what planets have a radius of 0.188']
for query in queries:
    q_xpath = translate_query(query,g)
    # query database with Xpath query
    planets = oec.findall(q_xpath)
    planet_names = [p.findtext('name') for p in planets]
    print(
        f'I found the following planet(s):{", ".join(planet_names)}\n')

