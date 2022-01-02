import wikipedia
import json

planets = ['earth','jupiter','neptune','saturn','uranus','mars','venus','Mercury (planet)']
summaries = dict()

for p in planets:
    print(p)
    summaries[p] = wikipedia.summary(p,auto_suggest=False)

with open('planets_wiki.json', 'w') as fp:
    json.dump(summaries, fp)
