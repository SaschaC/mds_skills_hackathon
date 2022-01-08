
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
VP[SEM=(?v + ?p)] -> TV[SEM=?v] NP[SEM=?p] | CMPLX-V[SEM=?v] PP[SEM=?p]
NP[SEM=(?det + ?n)] -> Art[SEM=?det] NP[SEM=?n] | Int[SEM=?det] N[SEM=?n]
NP[SEM=(?np + ?num)] -> NP[SEM=?np] PP[SEM=?num] | NP[SEM=?np] AP[SEM=?num]
PP[SEM=(?p + ?num)] -> P[SEM=?p] NUM[SEM=?num] | P[SEM=?p] ADVP[SEM=?num] 
ADVP[SEM=(?adv + ?num)] -> CMPLX-ADV[SEM=?adv] NUM[SEM=?num] 
AP[SEM=(?a + ?num)] -> CMPLX-A[SEM=?a] NUM[SEM=?num]
CMPLX-A[SEM=?a] -> A[SEM=?a] CONJ
CMPLX-ADV[SEM=?adv] -> ADV[SEM=?adv] CONJ | P ADV[SEM=?adv]
CMPLX-V[SEM=?part] -> AUX PART[SEM=?part]
PART[SEM='[discoveryyear'] -> 'discovered'
Int[SEM='.//'] -> 'which' | 'what'
AUX -> 'were'
TV[SEM=''] -> 'have' | 'possess'
Art[SEM=''] -> 'a'
NP[SEM='[mass'] -> 'mass'
NP[SEM='[radius'] -> 'radius'
N[SEM='planet'] -> 'planets'
P[SEM=''] -> 'of' |'at'
P[SEM='<'] -> 'before'
P[SEM='>'] -> 'after'
CONJ[SEM=''] -> 'than'
A[SEM='>'] -> 'bigger' | 'larger' | 'greater' 
A[SEM='<'] -> 'smaller'
ADV[SEM='<'] -> 'less' | 'most'
ADV[SEM='>'] -> 'more' | 'least'
NUM[SEM="=#NUM#]"] -> '#NUM#'
"""
# get xml exoplanet database:
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = etree.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

queries = ['what planets have a mass of 19.4','which planets have a mass of 19.4',
'what planets have a radius of 0.188','which planets have a mass of at least 19.4',
'which planets have a mass of at most 0.001','which planets have a mass smaller than 0.001',
'which planets have a mass greater than 19.4','what planets were discovered before 2010']
for query in queries:
    print(f'NL query: {query}')
    q_xpath = translate_query(query,g)
    # query database with Xpath query
    planets = oec.xpath(q_xpath)
    planet_names = get_names(planets)
    print(
        f'I found the following planet(s):{", ".join(planet_names)}\n')