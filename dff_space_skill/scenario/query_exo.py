
import nltk,urllib.request, gzip, io
from nltk import grammar, parse
from nltk.tokenize import word_tokenize
import re
from lxml import etree


def translate_query(query,g):
    # remove numbers from query and substitute by '#NUM#'
    numbers = re.findall(r'\d+\.*\d*',query)
    query = re.sub(r'\d+\.*\d*','#NUM#',query)
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

def get_names(elements):
    names = []
    for e in elements:
        aliasses = ''
        for name in e.xpath("name"):
            aliasses+=f'/{name.text}'
        names.append(aliasses[1:])
    return names

# grammar
g = """
% start S
S[SEM=(?np + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]
VP[SEM=(?v + ?np)] -> TV[SEM=?v] NP[SEM=?np]
NP[SEM=(?det + ?n)] -> Art[SEM=?det] NP[SEM=?n] | Int[SEM=?det] N[SEM=?n]
NP[SEM=(?np + ?pp)] -> NP[SEM=?np] PP[SEM=?pp]
PP[SEM=(?p + ?num)] -> P[SEM=?p] NUM[SEM=?num] | P[SEM=?p] AP[SEM=?num]
AP[SEM=(?a + ?num)] -> CMPLX-A[SEM=?a] NUM[SEM=?num]
CMPLX-A[SEM=(?p + ?a)] -> P[SEM=?p] A[SEM=?a] 
Int[SEM='.//'] -> 'which' | 'what'
TV[SEM=''] -> 'have'
Art[SEM=''] -> 'a'
NP[SEM='[mass'] -> 'mass'
NP[SEM='[radius'] -> 'radius'
N[SEM='planet'] -> 'planet' | 'planets'
P[SEM=''] -> 'of' |'at'
A[SEM='>'] -> 'least'
A[SEM='<'] -> 'most'
NUM[SEM="=#NUM#]"] -> '#NUM#'
"""
# get xml exoplanet database:
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

queries = ['what planets have a mass of 19.4','which planets have a mass of 19.4','what planets have a radius of 0.188','which planets have a mass of at least 19.4','which planets have a mass of at most 0.001']
for query in queries:
    q_xpath = translate_query(query,g)
    # query database with Xpath query
    planets = oec.xpath(q_xpath)
    planet_names = get_names(planets)
    print(
        f'I found the following planet(s):{", ".join(planet_names)}\n')