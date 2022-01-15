import nltk
from nltk import grammar, parse


g = """
% start S
S[SEM = <?subj(?vp)>] -> NP[NUM=?n,SEM=?subj] VP[NUM=?n,SEM=?vp]

VP[NUM=?n,SEM=?obj] -> TV[NUM=?n] NP[SEM=?obj]

NP[+INT,NUM=?n,SEM=<?det(?nom)>] -> Det[+INT, NUM=?n,SEM=?det]  Nom[NUM=?n,SEM=?nom]
NP[-INT,NUM=?n,SEM=?nom] -> Det[-INT, NUM=?n]  Nom[NUM=?n,SEM=?nom]
Nom[NUM=?n,SEM=?nom] -> N[NUM=?n,SEM=?nom]
Nom[NUM=?n,SEM=<?nom(?pp)>] -> N[NUM=?n,SEM=?nom] PP[SEM=?pp]
Nom[SEM=<?u(?a)>] -> A[SEM=?a] UNIT[SEM=?u]
PP[SEM=?nom] -> P[-LOC] Nom[SEM=?nom]

N[NUM=sg,SEM=<\\x.planet(x)>] -> 'planet'
N[NUM=pl,SEM=<\\x.planet(x)>] -> 'planets'
N[NUM=sg,SEM=<\\P x .exists y.(radius(x,y) & P(y))>] -> 'radius'
UNIT[SEM=<\\P.P(number)>] -> '#NUM#'
A[SEM=<\\x y.greater(x,y)>] -> 'greater'

Det[+INT,NUM=pl,SEM=<\\P \\Q.exists x.(P(x) & Q(x))>] -> 'which'
Det[+INT,NUM=sg,SEM=<\\P \\Q.exists x.(P(x) & Q(x))>] -> 'which'
Det[-INT,NUM=sg,SEM=<\\P \\Q.exists x.(P(x) & Q(x))>] -> 'a'

TV[NUM=sg,SEM="",TNS=pres] -> 'has'
TV[NUM=pl,SEM="",TNS=pres] -> 'have'

P[-LOC,SEM=""] -> 'of'

"""

sents = ['which planets have a radius of greater #NUM#']
gram = grammar.FeatureGrammar.fromstring(g)
parser = parse.FeatureEarleyChartParser(gram,trace=0)
trees = list(parser.parse(sents[0].split()))

for results in nltk.interpret_sents(sents, gram):
    for (synrep, semrep) in results:
        print(semrep)