g = """
% start S

S[SEM=?s,NUM=?num,L=?l] -> S1[SEM=?s,NUM=?num,L=?l] | S2[SEM=?s,NUM=?num,L=?l]
S1[SEM=('(.//' + ?n + ')' + '[position()<' + ?count + ']'),L=?l] -> N[BAR=2,NUM=?num,SEM=?n,COUNT=?count,L=?l]
S1[NUM=?num,SEM=(?s+ ';' + ?c),L=?l] -> S1[NUM=?num,SEM=?s,L=?l] CONJ[BAR=1,SEM=?c,L=?l]

S2[SEM=(?n + '[' + ?v+']'),NUM=?num,L=?l] -> N[BAR=2,SEM=?n,NUM=?num,L=?l] V[BAR=2,SEM=?v,NUM=?num,L=?l]
S2[NUM=?num,SEM=(?s+ ';' + ?c),L=?l] -> S2[NUM=?num,SEM=?s,L=?l] CONJ[BAR=1,SEM=?c,L=?l]

V[BAR=2,SEM=(?v + ?n),NUM=?num,L=?l] -> V[BAR=1,SEM=?v,NUM=?num,L=?l] N[BAR=2,SEM=?n,L=?l]
V[BAR=2,SEM=(?v + ?n),NUM=?num,L='de',+VFINAL] -> N[BAR=2,SEM=?n] V[BAR=1,SEM=?v,NUM=?num,L='de']
V[BAR=2,SEM=(?v + ?p),NUM=?num,L=?l] -> V[BAR=1,SEM=?v,NUM=?num,L=?l] P[BAR=2,SEM=?p,SUBC=?subc,L=?l]
V[BAR=2,SEM=(?v + ?p),NUM=?num,L='de',+VFINAL] -> P[BAR=2,SEM=?p,SUBC=?subc,L='de'] V[BAR=1,SEM=?v,NUM=?num,L='de',+VFINAL]
V[BAR=2,SEM=(?v + ?c),NUM=?num,L=?l] -> V[BAR=1,SEM=?v,NUM=?num,L=?l] CONJ[BAR=2,SEM=?c,L=?l]
V[BAR=1,SEM=?p] -> AUX PART[SEM=?p,L=?l]
V[BAR=1,SEM=?p,L='de',+VFINAL] -> PART[SEM=?p,L='de'] AUX[L='de']
V[BAR=1,SEM='',L='de'] -> AUX[L='de']
V[BAR=1,SEM=?v,NUM=?num,L=?l] -> V[BAR=0,SEM=?v,NUM=?num,L=?l]

C[BAR=2,SEM=?v,NUM=?num,L=?l] -> C[BAR=1,L=?l] V[BAR=2,SEM=?v,NUM=?num,L=?l]
C[BAR=2,SEM=?v,NUM=?num,L='de'] -> C[BAR=1,L='de'] V[BAR=2,SEM=?v,NUM=?num,L='de',+VFINAL]
C[BAR=2,SEM=?c,L=?l] -> C[BAR=1,L=?l] CONJ[BAR=2,SEM=?c,L=?l]
C[BAR=1,L=?l] -> C[BAR=0,L=?l]

CONJ[BAR=2,SEM=(?n + ?c),L=?l] -> N[BAR=2,SEM=?n,L=?l] CONJ[BAR=1,SEM=?c,L=?l]
CONJ[BAR=2,SEM=(?v + ?c),L=?l] -> V[BAR=2,SEM=?v,L=?l] CONJ[BAR=1,SEM=?c,L=?l]
CONJ[BAR=2,SEM=(?p + ?c),L=?l] -> P[BAR=2,SEM=?p,SUBC=?subc,L=?l] CONJ[BAR=1,SEM=?c,L=?l]
CONJ[BAR=2,SEM=(?c + ?con),L=?l] -> C[BAR=2,SEM=?c,L=?l] CONJ[BAR=1,SEM=?con,L=?l]
CONJ[BAR=1,SEM=(?c+ ?cp),L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] CONJ[BAR=2,SEM=?cp,L=?l] 
CONJ[BAR=1,SEM=(?c + ?n),L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] N[BAR=2,SEM=?n,L=?l]
CONJ[BAR=1,SEM=(?c + ?n),L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] N[BAR=2,SEM=?n,L=?l]
CONJ[BAR=1,SEM=(?c + ?v),L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] V[BAR=2,SEM=?v,L=?l]
CONJ[BAR=1,SEM=(?c + ?v),L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] P[BAR=2,SEM=?v,SUBC=?subc,L=?l]
CONJ[BAR=1,SEM=(?con + ?c),L=?l] -> CONJ[BAR=0,SEM=?con,L=?l] C[BAR=2,SEM=?c,L=?l]
CONJ[BAR=1,SEM=?s,L=?l] -> CONJ[BAR=0,SEM=?c,L=?l] S[SEM=?s,L=?l]

N[BAR=2,NUM=?num,SEM=(?det + ?n),COUNT='=count(//*)',L=?l] -> Art[NUM=?num,SEM=?det,L=?l] N[BAR=1,NUM=?num,SEM=?n,L=?l] | Int[NUM=?num,SEM=?det,L=?l] N[BAR=1,NUM=?num,SEM=?n,L=?l]
N[BAR=2,NUM=?num,SEM=?n,COUNT=?count,L=?l] -> Num[SEM=?count,L=?l] N[BAR=1,NUM=?num,SEM=?n,L=?l]
N[BAR=2,SEM=(?n + ' and ' + ?c),NUM=?num,COUNT='=count(//*)',L=?l] -> N[BAR=2,SEM=?n,NUM=?num,L=?l] C[BAR=2,SEM=?c,NUM=?num,L=?l]
N[BAR=2,SEM=(?a + ?n),L=?l] -> A[BAR=2,SEM=?a,L=?l] N[BAR=1,SEM=?n,L=?l]
N[BAR=1,SEM=(?n + ?p),L=?l] -> N[BAR=0,SEM=?n,L=?l] P[BAR=2,SEM=?p,SUBC='-Adj',L=?l]
N[BAR=1,SEM=(?n + '[' + ?p +']'),L=?l] -> N[BAR=1,SEM=?n,L=?l] P[BAR=2,SEM=?p,SUBC='+Adj',L=?l]
N[BAR=1,SEM=(?n + '[' + ?c +']'),L=?l] -> N[BAR=0,SEM=?n,L=?l] C[BAR=2,SEM=?c,L=?l]
N[BAR=1,SEM=(?n + ?a),L=?l] -> N[BAR=0,SEM=?n,L=?l] A[BAR=2,SEM=?a,L=?l]
N[BAR=1,NUM=?num,SEM=?n,L=?l] -> N[BAR=0,NUM=?num,SEM=?n,L=?l]

P[BAR=2,SEM=(?p + ?n),SUBC=?subc,L=?l] -> P[BAR=1,SEM=?p,SUBC=?subc,L=?l] A[BAR=2,SEM=?n,L=?l]
P[BAR=2,SEM=(?p + ?n),SUBC=?subc,L=?l] -> P[BAR=1,SEM=?p,SUBC=?subc,L=?l] N[BAR=2,SEM=?n,L=?l]
P[BAR=2,SEM=(?p + ?n),SUBC=?subc,L=?l] -> P[BAR=1,SEM=?p,SUBC=?subc,L=?l] Num[SEM=?n,L=?l]
P[BAR=2,SEM=(?s + ?p + ?n),SUBC=?subc,L='de'] -> P[BAR=1,SEM=?p,SUBC=?subc,L='de'] Num[SEM=?n] PART[SEM=?s,L='de']
P[BAR=2,SEM=(?p + ?c),SUBC=?subc,L=?l] -> P[BAR=1,SEM=?p,SUBC=?subc,L=?l] CONJ[BAR=2,SEM=?c,L=?l]

P[BAR=1,SEM=?p,SUBC=?subc,L=?l] -> P[BAR=0,SEM=?p,SUBC=?subc,L=?l]

A[BAR=2,SEM=(?a+?n),L=?l] -> A[BAR=1,SEM=?a,L=?l] Num[SEM=?n,L=?l]
A[BAR=1,SEM=?a,L=?l] -> A[BAR=0,SEM=?a,L=?l]
A[BAR=1,SEM=?a,L=?l] -> A[BAR=0,SEM=?a,L=?l] CONJ[BAR=0,L=?l]
A[BAR=1,SEM=?a,L=?l] -> P[BAR=1,L=?l] A[BAR=1,SEM=?a,L=?l]

PART[SEM='discoveryyear',L='en'] -> 'discovered'
Int[NUM='sg',SEM='.//',L='en'] -> 'which' | 'what'
Int[NUM='pl',SEM='.//',L='en'] -> 'which' | 'what'
AUX[NUM='pl',L='en'] -> 'were'
AUX[NUM='sg',L='en'] -> 'was'
V[NUM='pl',BAR=0,SEM='',L='en'] -> 'have' | 'possess'
V[NUM='sg',BAR=0,SEM='',L='en'] -> 'has' | 'possesses'
Art[NUM='sg',SEM='',L='en'] -> 'a' | 'any' | 'an'
Art[NUM='pl',SEM='',L='en'] -> | 'any'
N[BAR=0,NUM='sg',SEM='mass',L='en'] -> 'mass'
N[BAR=0,NUM='sg',SEM='radius',L='en'] -> 'radius'
N[BAR=0,NUM='sg',SEM='age',L='en'] -> 'age'
N[BAR=0,NUM='sg',SEM='temperature',L='en'] -> 'temperature'
N[NUM='pl',BAR=0,SEM='planet',L='en'] -> 'planets'
N[NUM='sg',BAR=0,SEM='planet',L='en'] -> 'planet'
Num[NUM='na',SEM="=#NUM#"] -> '#num#'
Num[NUM='na',SEM="=#NUM0"] -> '#num0'
Num[NUM='na',SEM="=#NUM1"] -> '#num1'
Num[NUM='na',SEM="=#NUM2"] -> '#num2'
Num[NUM='na',SEM="=#NUM3"] -> '#num3'
Num[NUM='na',SEM="=#NUM4"] -> '#num4'
Num[NUM='na',SEM="=#NUM5"] -> '#num5'
Num[NUM='na',SEM="=#NUM6"] -> '#num6'
Num[NUM='na',SEM="=#NUM7"] -> '#num7'
Num[NUM='na',SEM="=#NUM8"] -> '#num8'
Num[NUM='na',SEM="=#NUM9"] -> '#num9'
Num[NUM='na',SEM="=#NUM10"] -> '#num10'
P[BAR=0,SEM='',SUBC='-Adj',L='en'] -> 'of' |'at'
P[BAR=0,SEM='<',SUBC='-Adj',L='en'] -> 'before'
P[BAR=0,SEM='>',SUBC='-Adj',L='en'] -> 'after'
P[BAR=0,SEM='',SUBC='-Adj',L='en'] -> 'in'
P[BAR=0,SEM='',SUBC='+Adj',L='en'] -> 'with'
C[BAR=0,L='en'] -> 'that' | 'which'
CONJ[BAR=0,SEM='',L='en'] -> 'than'
CONJ[BAR=0,SEM=' and ',L='en'] -> 'and'
A[BAR=0,SEM='>',L='en'] -> 'bigger' | 'larger' | 'greater' | 'more' | 'least' | 'above' | 'over'
A[BAR=0,SEM='<',L='en'] -> 'smaller' | 'less' | 'most' | 'maximally' | 'below' | 'under'

PART[SEM='discoveryyear',L='de'] -> 'entdeckt'
Int[NUM='sg',SEM='.//',L='de'] -> 'welcher'
Int[NUM='pl',SEM='.//',L='de'] -> 'welche'
AUX[NUM='pl',L='de'] -> 'wurden'
AUX[NUM='sg',L='de'] -> 'wurde'
V[NUM='pl',BAR=0,SEM='',L='de'] -> 'haben' | 'besitzen'
V[NUM='sg',BAR=0,SEM='',L='de'] -> 'hat' | 'besitzt'
Art[NUM='sg',SEM='',L='de'] -> 'ein' | 'einen' | 'eine' | 'einem' | 'einer'
Art[NUM='pl',SEM='',L='de'] -> 
N[BAR=0,NUM='sg',SEM='mass',L='de'] -> 'masse'
N[BAR=0,NUM='sg',SEM='radius',L='de'] -> 'radius'
N[BAR=0,NUM='sg',SEM='age',L='de'] -> 'alter'
N[BAR=0,NUM='sg',SEM='temperature',L='en'] -> 'temperatur'
N[NUM='pl',BAR=0,SEM='planet',L='de'] -> 'planeten'
N[NUM='sg',BAR=0,SEM='planet',L='de'] -> 'planet'
P[BAR=0,SEM='',SUBC='-Adj',L='de'] -> 'von'
P[BAR=0,SEM='<',SUBC='-Adj',L='de'] -> 'vor'
P[BAR=0,SEM='>',SUBC='-Adj',L='de'] -> 'nach'
P[BAR=0,SEM='',SUBC='-Adj',L='de'] -> 'in'
P[BAR=0,SEM='',SUBC='+Adj',L='de'] -> 'mit'
C[BAR=0,L='de'] -> 'der' | 'die'
CONJ[BAR=0,SEM='',L='de'] -> 'als'
CONJ[BAR=0,SEM=' and ',L='de'] -> 'und'
A[BAR=0,SEM='>',L='de'] -> 'größer' | 'mehr' | 'mindestens' | 'über'
A[BAR=0,SEM='<',L='de'] -> 'kleiner' | 'weniger' | 'maximal' | 'unter'
"""