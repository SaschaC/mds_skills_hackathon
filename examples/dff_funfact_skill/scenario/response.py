import random

from df_engine.core import Actor, Context


FUNFACT_LIST = [
    ("Pineapple works as a natural meat tenderizer.", "food"),
    ("Only two mammals like spicy food: humans and the tree shrew.", "food"),
    ("The M in M&Ms stand for Mars and Murrie.", "food"),
    ("Pringles are not actually potato chips.", "food"),
    ("Cotton candy was invented by a dentist.", "food"),
    ("Water makes different pouring sounds depending on its temperature.", "food"),
    ("Some sea snakes can breathe through their skin.", "animals"),
    ('The budget for the Movie "Titanic" was higher than the budget of Titanic itself.', "movies"),
    ("The original London Bridge is now in Arizona.", "travelling"),
    ("The healthiest place in the world is in Panama.", "travelling"),
    ("Pigeons can tell the difference between a painting by Monet and Picasso.", "travelling"),
    ("Dinosaurs lived on every continent.", "travelling"),
    ("Napoleon was once attacked by thousands of rabbits.", "travelling"),
    (
        "For 100 years, maps have shown an island that does not exist. Sandy Island about size of Manhattan"
        " in the Pacific Ocean was discovered in 1774, but in 2012 it turned out to not exist",
        "travelling",
    ),
    ("A 2007 study found that music, classical in particular, can help make plants grow faster.", "music"),
    (
        "The world’s largest book made of paper is located in Dubai, United Arab Emirates. "
        "It is five meters wide, 8.06 meters long, contains 429 pages and weighs over 3,000 pounds.",
        "books",
    ),
    (
        "Australian rower Bobby Pearce won the 1928 Olympic Games against eight other competitors, "
        "even though he stopped during the race to let ducks pass in front of him.",
        "sport",
    ),
    ("The sunniest place on earth is Arizona.", "weather"),
    ("The hottest spot on the planet is in Libya.", "weather"),
    (
        "The oldest continuously published daily newspaper in the United States is the New York Post, "
        "which was founded in 1801 by Alexander Hamilton.",
        "news",
    ),
    ("Marie Curie is the only person to earn a Nobel prize in two different sciences.", "science"),
    ("Showers really do spark creativity.", "science"),
    ("Dogs actually understand some English.", "science"),
    (
        "South Korea has a rule called ‘Cinderella law’ which disallows under-16 gamers "
        "to play online video games after midnight.",
        "games",
    ),
]


def random_planet_fact(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    fact, topic = random.sample(FUNFACT_LIST, 1)[0]
    question = "Would you like to hear another fun fact?"
    return f"{fact} {question}"
