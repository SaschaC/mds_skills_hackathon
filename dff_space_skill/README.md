# dff-space-skill

## Description

**dff-space-skill** can query a database of exoplanets with natural language queries in English and German. For example, you can ask: 
* 'What planets were discovered in 2020?'
* 'Are there any planets with a radius smaller than 0.1?'

Or more complex queries with several conjunctions: 
* 'Which planets that were discovered before 2010 have a radius of at least 1 and a mass of at most 5?'
* 'Show me 5 planets with a mass smaller than 2 and a radius of at least 1 and 3 planets that were discovered before 2010'.

You can use the similar queries in German:
* 'Welche Planeten wurden in 2020 entdeckt?'
* 'Gibt es Planeten mit einem Radius kleiner als 0.1?'
* 'Welche Planeten, die vor 2010 entdeckt wurden, haben einen Radius von mindestens 1 und eine Masse von maximal 5?'
* 'Zeig mir 5 Planeten mit einer Masse von maximal 2 und 3 Planeten, die vor 2010 entdeckt wurden'

You can run the python run_test.py to get some more examples of query types.

The parameters that can be used in the queries are numeric and they are radius (de: 'radius'), mass (de: 'Masse'), age (de: 'Alter'), discovered (de: 'entdeckt'), and temperature (de: 'Temperatur'). Radius and mass are derived from Jupiter. Age is measured in Gyr (1 Billion years) and temperature in Calvin. For more info visit:
[Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/)

For each query result, the dialogue agent asks if you want get more details on a specific planet. You can then pick a planet to receive a brief summary of its interesting features.

## Quickstart

```bash
pip install -r requirements.txt
```
Run interactive mode
```bash
python run_interactive.py
```
Run tests
```bash
python run_test.py
```