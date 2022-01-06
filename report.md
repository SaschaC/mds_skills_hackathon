<!-- 
Instructions: 
- The report (report.md/report.ipynb ) should be in the root of your repository of a project
- The link to the repository have to be shared with us 
- Weekly report can be built in md-file or ipynb file 
- All reports for each week should be written into one file 
- Each week should be in a separated section in the file, see as shown in this file 
- The report should contain subsections TODO / WIP (work in progress) / Done / Issues 
- Each section should contain a list of works and their descriptions 
- Adding pictures / graphs / code inserts to md / ipynb cells can improve your report 
- The deadline is 11.59 pm UTC -12h (anywhere on earth)
 -->
 
# Week 1

TODO:
 - My skill will comprise 3 parts: random fact generation for the 8 planets in our solar system based on scraped web data, Mars weather information based on NASA API, exoplanet search based on NASA API and others.  
   - Step 1: data gathering, API search, conceptualization of the skills.
   - Step 2: developping dialogue flow for natural language queries in exoplanet search and Mars weather information.
   - Step 3:  Implement search execution based on natural language queries provided by user. 
   - Step 4: Expand dialogue flow to customize presentation of search results.
   - Step 5: Implement different scenarios of search result presentation.
   - Step 6 (optional): Research methods for Natural language to database query conversion and implment one method.  
 
WIP:
 - I am gathering different data sources to use for the exoplanet search. Sources I will use are:
   - [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS)
   - [Exoplanet Open Catalogue](http://www.openexoplanetcatalogue.com/planet/11%20Com%20b/)
   - [Mars Weather API](https://mars.nasa.gov/insight/weather/)
 - I am working on the dialogue flow to provide search parameters by the user for exoplanet search.  

Done:
 - I implemented a basic dialogue flow.
 - I scraped data from Wikipedia.
 - The assistant generates random facts for any of the 8 planets in our solar system based on the scraped Wikipedia data.

# Week 2

TODO:
 - Natural language expoplanet querying:
  - Create list of possible query types
  - Further develop context free grammar for NL to XPath translation 
  - Create custom functions for more complex searches not supported by ElementTree package or use libxml2 package instead.
 - Develop dialogue flow to guide user queries. For example, adding the possibility to request more info for a given search result, save search results.
 - Start Mars Weather querying implementation.

WIP:
 - Work on context free grammar for exoplanet querying.

Done:
 - Familiarized myself with the [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) package
 - Studied CFG implmentation on NLTK website
 - I created a CFG prototype for simple exoplanet queries under ./scenarios

# Week 3
....

# Week 4
....
