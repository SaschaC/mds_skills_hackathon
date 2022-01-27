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
    ("no","OK bye!")]
]

def run_test():
    ctx = {}
    for testing_dialog in test_set:
        for in_request, true_out_response in testing_dialog:
            _, ctx = run_interactive.turn_handler(in_request, ctx, actor, true_out_response=true_out_response)
        print("test passed")

if __name__ == "__main__":
    run_test()