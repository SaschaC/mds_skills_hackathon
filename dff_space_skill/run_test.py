import random

from scenario.main import actor
import run_interactive

random.seed(314)

# testing


test_set = [
    [("hi", "Please enter your search query!"),
    ("planets with a radius of at most 0.05","""

Normalized NL Query: planets with a radius of at most #num0
XML Queries:['(.//planet[radius<=0.05])[position()<=count(//*)]']

I found the following 13 planets for the query 'planets with a radius of at most 0.05':

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Would you like more info on one of these planets?
"""
    ),
    ("yes", "Alright, for which planet?"),
    ("KOI-115.03","\n\nKOI-115.03 is an unconfirmed transiting planet orbiting Kepler-105.\n\nWould you like to try another search?\n"),
    ("no","OK bye!")
    ],
[("hi", "Please enter your search query!"),("Are there any planets with a radius of at most 0.05?","""

Normalized NL Query:  planets with a radius of at most #num0
XML Queries:['(.//planet[radius<=0.05])[position()<=count(//*)]']

I found the following 13 planets for the query 'Are there any planets with a radius of at most 0.05?':

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
    [("hi", "Please enter your search query!"),("Which planets have a radius of at most 0.05?","""

Normalized NL Query: which planets have a radius of at most #num0
XML Queries:['.//planet[radius<=0.05]']

I found the following 13 planets for the query 'Which planets have a radius of at most 0.05?':

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
    [("hi", "Please enter your search query!"),("show me 2 planets with a radius below 0.05","""

Normalized NL Query:  #num0 planets with a radius below #num1
XML Queries:['(.//planet[radius<=0.05])[position()<=2]']

I found the following 2 planets for the query 'show me 2 planets with a radius below 0.05':

Kepler-102 b, KOI-115.03

Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
        [("hi", "Please enter your search query!"),("show me 3 planets with a radius of at least 1 and a mass of at most 5 that were discovered before 2020","""

Normalized NL Query:  #num0 planets with a radius of at least #num1 and a mass of at most #num2 that were discovered before #num3
XML Queries:['(.//planet[radius>=1 and mass<=5 and discoveryyear<=2020])[position()<=3]']

I found the following 3 planets for the query 'show me 3 planets with a radius of at least 1 and a mass of at most 5 that were discovered before 2020':

51 Eri b, CoRoT-11 b, CoRoT-12 b

Would you like more info on one of these planets?
"""
    ),
    ("yes", "Alright, for which planet?"),
    ("51 Eri b","""

51 Eri b is a directly-imaged exoplanet located at a projected separation of 13.2 AU from its star. The system also exhibits an infrared excess indicating the presence of debris belts at around 5.5 AU and 82 AU from the star. It is a member of the Beta Pictoris moving group.

Would you like to try another search?
"""), ("no","OK bye!")],
[("hi", "Please enter your search query!"),("Show me 1 planet with an age of maximally 0.1 and a mass of at least 1 that was discovered in 2020 and 3 planets that have a radius of at least 1",
"""

Normalized NL Query:  #num0 planet with an age of maximally #num1 and a mass of at least #num2 that was discovered in #num3 and #num4 planets that have a radius of at least #num5
XML Queries:['(.//planet[age<=0.1 and mass>=1 and discoveryyear=2020])[position()<=1]', '(.//planet[radius>=1])[position()<=3]']

I did not find any planet for part 1 of the query 'Show me 1 planet with an age of maximally 0.1 and a mass of at least 1 that was discovered in 2020 and 3 planets that have a radius of at least 1'.

Here are 3 planets I found for part 2 of the query 'Show me 1 planet with an age of maximally 0.1 and a mass of at least 1 that was discovered in 2020 and 3 planets that have a radius of at least 1':

1RXS1609 b, 2M 2206-20 b, 2MASS J0219-3925 B


Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
[("hi", "Please enter your search query!"),("Show me 3 planets that were discovered before 2020 and that have a mass of at least 2 with an age of maximally 5.",
"""

Normalized NL Query:  #num0 planets that were discovered before #num1 and that have a mass of at least #num2 with an age of maximally #num3
XML Queries:['(.//planet[discoveryyear<=2020 and mass>=2][age<=5.])[position()<=3]']

I found the following 3 planets for the query 'Show me 3 planets that were discovered before 2020 and that have a mass of at least 2 with an age of maximally 5.':

HD 100546 b, SDSS J1110+0116, SIMP0136+0933

Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
[("hi", "Please enter your search query!"),("which planets have a mass of 1 and which planets were discovered before 2001 and which planets have a mass of 1 and were discovered before 2001?",
"""

Normalized NL Query: which planets have a mass of #num0 and which planets were discovered before #num1 and which planets have a mass of #num2 and were discovered before #num3
XML Queries:['.//planet[mass=1]', './/planet[discoveryyear<=2001]', './/planet[mass=1 and discoveryyear<=2001]']

Here are 6 planets I found for part 1 of the query 'which planets have a mass of 1 and which planets were discovered before 2001 and which planets have a mass of 1 and were discovered before 2001?':

HD 219415 b, HD 75784 b, Kepler-44 b, Jupiter, WASP-129 b, WASP-190 b

Here are 66 planets I found for part 2 of the query 'which planets have a mass of 1 and which planets were discovered before 2001 and which planets have a mass of 1 and were discovered before 2001?':

16 Cygni B b, 47 UMa b, 47 UMa c, 51 Peg b, 55 Cancri b, 70 Vir b, BD-10 3166 b, eps Eridani b, Gliese 3021 A b, Gliese 86 b, Gliese 876 b, Gliese 876 c, HD 10697 b, HD 114762 b, HD 114783 b, HD 12661 b, HD 130322 b, HD 134987 b, HD 142 A b, HD 16141 A b, HD 168443 b, HD 168443 c, HD 169830 b, HD 177830 A b, HD 178911 B b, HD 179949 b, HD 187123 b, HD 192263 b, HD 195019 A b, HD 19994 A b, HD 209458 b, HD 210277 b, HD 213240 A b, HD 217107 b, HD 222582 A b, HD 23079 b, HD 27442 A b, HD 28185 b, HD 37124 b, HD 38529 A b, HD 39091 b, HD 4203 b, HD 4208 b, HD 46375 A b, HD 52265 b, HD 6434 b, HD 68988 b, HD 75289 A b, HD 80606 b, HD 89744 A b, HD 92788 b, HR 810 b, ITG 15B, mu Arae b, PSR 1257+12 A, PSR 1257+12 B, PSR 1257+12 C, PSR B1620-26 b, Rho Coronae Borealis b, Uranus, Neptune, Pluto, tau Boo A b, Upsilon Andromedae A b, Upsilon Andromedae A c, Upsilon Andromedae A d

I did not find any planet for part 3 of the query 'which planets have a mass of 1 and which planets were discovered before 2001 and which planets have a mass of 1 and were discovered before 2001?'.


Would you like more info on one of these planets?
"""
    ),
    ("no", "Would you like to try another search?"),
    ("no","OK bye!")],
[("hi", "Please enter your search query!"),
    ("Planeten mit einem Radius von maximal 0.05","""

Normalized NL Query: planeten mit einem radius von maximal #num0
XML Queries:['(.//planet[radius<=0.05])[position()<=count(//*)]']

Ich habe die folgenden 13 Planeten gefunden für die Anfrage 'Planeten mit einem Radius von maximal 0.05:'

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Gibt es Planeten mit einem Radius von maximal 0.05?","""

Normalized NL Query:  planeten mit einem radius von maximal #num0
XML Queries:['(.//planet[radius<=0.05])[position()<=count(//*)]']

Ich habe die folgenden 13 Planeten gefunden für die Anfrage 'Gibt es Planeten mit einem Radius von maximal 0.05?:'

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Gibt es Planeten mit einem Radius von maximal 0.05?","""

Normalized NL Query:  planeten mit einem radius von maximal #num0
XML Queries:['(.//planet[radius<=0.05])[position()<=count(//*)]']

Ich habe die folgenden 13 Planeten gefunden für die Anfrage 'Gibt es Planeten mit einem Radius von maximal 0.05?:'

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Welche Planeten haben einen Radius von unter 0.05?","""

Normalized NL Query: welche planeten haben einen radius von unter #num0
XML Queries:['.//planet[radius<=0.05]']

Ich habe die folgenden 13 Planeten gefunden für die Anfrage 'Welche Planeten haben einen Radius von unter 0.05?:'

Kepler-102 b, KOI-115.03, Kepler-1308 b, Kepler-37 b, Kepler-444 b, Kepler-444 c, Kepler-444 d, Kepler-444 e, Kepler-62 c, Kepler-138 b, Mercury, Mars, Pluto

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Zeig mir 2 Planeten mit einem Radius von weniger als 0.05","""

Normalized NL Query:  #num0 planeten mit einem radius von weniger als #num1
XML Queries:['(.//planet[radius<=0.05])[position()<=2]']

Ich habe die folgenden 2 Planeten gefunden für die Anfrage 'Zeig mir 2 Planeten mit einem Radius von weniger als 0.05:'

Kepler-102 b, KOI-115.03

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Zeig mir 3 Planeten mit einem Radius von mindestens 1 und einer Masse von maximal 5, die vor 2020 entdeckt wurden.","""

Normalized NL Query:  #num0 planeten mit einem radius von mindestens #num1 und einer masse von maximal #num2 die vor #num3 entdeckt wurden
XML Queries:['(.//planet[radius>=1 and mass<=5 and discoveryyear<=2020])[position()<=3]']

Ich habe die folgenden 3 Planeten gefunden für die Anfrage 'Zeig mir 3 Planeten mit einem Radius von mindestens 1 und einer Masse von maximal 5, die vor 2020 entdeckt wurden.:'

51 Eri b, CoRoT-11 b, CoRoT-12 b

Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Zeig mir 1 Planeten mit einem Alter von weniger als 0.1 und einer Masse von mehr als 1, der in 2020 entdeckt wurde, und 3 Planeten, die einen Radius von mindestens 1 haben.","""

Normalized NL Query:  #num0 planeten mit einem alter von weniger als #num1 und einer masse von mehr als #num2 der in #num3 entdeckt wurde und #num4 planeten die einen radius von mindestens #num5 haben
XML Queries:['(.//planet[age<=0.1 and mass>=1 and discoveryyear=2020])[position()<=1]', '(.//planet[radius>=1])[position()<=3]']

Ich habe keine Planeten für Teil 1 der Anfrage 'Zeig mir 1 Planeten mit einem Alter von weniger als 0.1 und einer Masse von mehr als 1, der in 2020 entdeckt wurde, und 3 Planeten, die einen Radius von mindestens 1 haben.' gefunden.

Hier sind 3 Planeten, die ich für Teil 2 der Anfrage 'Zeig mir 1 Planeten mit einem Alter von weniger als 0.1 und einer Masse von mehr als 1, der in 2020 entdeckt wurde, und 3 Planeten, die einen Radius von mindestens 1 haben.' gefunden habe:

1RXS1609 b, 2M 2206-20 b, 2MASS J0219-3925 B


Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
[("hi", "Bitte gib deine Anfrage ein."),
    ("Welche Planeten haben eine Masse von 1 und welche Planeten wurden vor 2001 entdeckt und welche Planeten haben eine Masse von 1 und wurden vor 2001 entdeckt?","""

Normalized NL Query: welche planeten haben eine masse von #num0 und welche planeten wurden vor #num1 entdeckt und welche planeten haben eine masse von #num2 und wurden vor #num3 entdeckt
XML Queries:['.//planet[mass=1]', './/planet[discoveryyear<=2001]', './/planet[mass=1 and discoveryyear<=2001]']

Hier sind 6 Planeten, die ich für Teil 1 der Anfrage 'Welche Planeten haben eine Masse von 1 und welche Planeten wurden vor 2001 entdeckt und welche Planeten haben eine Masse von 1 und wurden vor 2001 entdeckt?' gefunden habe:

HD 219415 b, HD 75784 b, Kepler-44 b, Jupiter, WASP-129 b, WASP-190 b

Hier sind 66 Planeten, die ich für Teil 2 der Anfrage 'Welche Planeten haben eine Masse von 1 und welche Planeten wurden vor 2001 entdeckt und welche Planeten haben eine Masse von 1 und wurden vor 2001 entdeckt?' gefunden habe:

16 Cygni B b, 47 UMa b, 47 UMa c, 51 Peg b, 55 Cancri b, 70 Vir b, BD-10 3166 b, eps Eridani b, Gliese 3021 A b, Gliese 86 b, Gliese 876 b, Gliese 876 c, HD 10697 b, HD 114762 b, HD 114783 b, HD 12661 b, HD 130322 b, HD 134987 b, HD 142 A b, HD 16141 A b, HD 168443 b, HD 168443 c, HD 169830 b, HD 177830 A b, HD 178911 B b, HD 179949 b, HD 187123 b, HD 192263 b, HD 195019 A b, HD 19994 A b, HD 209458 b, HD 210277 b, HD 213240 A b, HD 217107 b, HD 222582 A b, HD 23079 b, HD 27442 A b, HD 28185 b, HD 37124 b, HD 38529 A b, HD 39091 b, HD 4203 b, HD 4208 b, HD 46375 A b, HD 52265 b, HD 6434 b, HD 68988 b, HD 75289 A b, HD 80606 b, HD 89744 A b, HD 92788 b, HR 810 b, ITG 15B, mu Arae b, PSR 1257+12 A, PSR 1257+12 B, PSR 1257+12 C, PSR B1620-26 b, Rho Coronae Borealis b, Uranus, Neptune, Pluto, tau Boo A b, Upsilon Andromedae A b, Upsilon Andromedae A c, Upsilon Andromedae A d

Ich habe keine Planeten für Teil 3 der Anfrage 'Welche Planeten haben eine Masse von 1 und welche Planeten wurden vor 2001 entdeckt und welche Planeten haben eine Masse von 1 und wurden vor 2001 entdeckt?' gefunden.


Möchtest du mehr über einen dieser Planeten erfahren?
"""
    ),
    ("nein", "Möchtest du eine neue Suche starten?"),
    ("nein","OK bye!")
    ],
]

def run_test():
    ctx = {}
    for i,testing_dialog in enumerate(test_set):
        print(f'\n\n\n######################## TEST {i} ########################\n\n')
        for in_request,true_out_response in testing_dialog:
            _, ctx = run_interactive.turn_handler(in_request, ctx, actor, true_out_response=true_out_response)
        print("test passed")

if __name__ == "__main__":
    run_test()