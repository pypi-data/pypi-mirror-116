'''
Created on 2020-09-23

@author: wf
'''
import re
import time
from lodstorage.sparql import SPARQL

class Wikidata(object):
    '''
    Wikidata access
    '''

    def __init__(self, endpoint='https://query.wikidata.org/sparql'):
        '''
        Constructor
        '''
        self.endpoint=endpoint
        
    def getCityPopulations(self, profile=True):
        '''
        get the city populations from Wikidata
        
        Args:
            profile(bool): if True show profiling information
        '''  
        queryString="""
# get a list of human settlements having a geoName identifier
# to add to geograpy3 library
# see https://github.com/somnathrakshit/geograpy3/issues/15        
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
SELECT ?city ?cityLabel ?cityPop ?geoNameId ?country ?countryLabel ?countryIsoCode ?countryPopulation
WHERE {
  # geoName Identifier
  ?city wdt:P1566 ?geoNameId.
  # instance of human settlement https://www.wikidata.org/wiki/Q486972
  ?city wdt:P31/wdt:P279* wd:Q486972 .
  # population of city
  OPTIONAL { ?city wdt:P1082 ?cityPop.}

  # label of the City
  ?city rdfs:label ?cityLabel filter (lang(?cityLabel) = "en").
  # country this city belongs to
  ?city wdt:P17 ?country .
  # label for the country
  ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en").
  # https://www.wikidata.org/wiki/Property:P297 ISO 3166-1 alpha-2 code
  ?country wdt:P297 ?countryIsoCode.
  # population of country
  ?country wdt:P1082 ?countryPopulation.
  OPTIONAL {
     ?country wdt:P2132 ?countryGdpPerCapita.
  }
}"""      
        if profile:
            print("getting cities with population and geoNamesId from wikidata endpoint %s" %self.endpoint)
        starttime=time.time()
        wd=SPARQL(self.endpoint)
        results=wd.query(queryString)
        cityList=wd.asListOfDicts(results)
        if profile:
            print("Found %d cities  in %5.1f s" % (len(cityList),time.time()-starttime))
        return cityList
         
        
    def getCities(self,region=None, country=None):
        '''
        get the cities from Wikidata

        Args:
            region: List of countryWikiDataIDs. Limits the returned cities to the given countries
            country: List of regionWikiDataIDs. Limits the returned cities to the given regions
        '''
        values=""
        if region is not None:

            values+=Wikidata.getValuesClause("region", region)
        if country is not None:
            values+=Wikidata.getValuesClause("country", country)
        queryString="""# get a list of cities for the given region
# for geograpy3 library
# see https://github.com/somnathrakshit/geograpy3/issues/15
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
SELECT DISTINCT ?city ?cityLabel ?geoNameId ?cityPop ?cityCoord ?region ?regionLabel ?regionIsoCode ?country ?countryLabel ?countryIsoCode ?countryPopulation ?countryGdpPerCapita
WHERE {  
  # administrative unit of first order
  # example DE-NW Q1198
  %s
  #?region wdt:P31/wdt:P279* wd:Q10864048.
  ?region rdfs:label ?regionLabel filter (lang(?regionLabel) = "en").
  # isocode state/province
  OPTIONAL { ?region wdt:P300 ?regionIsoCode. }
  # country this region belongs to
  ?region wdt:P17 ?country .
  # label for the country
  ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en").
  # https://www.wikidata.org/wiki/Property:P297 ISO 3166-1 alpha-2 code
  ?country wdt:P297 ?countryIsoCode.
  # population of country
  ?country wdt:P1082 ?countryPopulation.
  OPTIONAL {
     ?country wdt:P2132 ?countryGdpPerCapita.
  }
  # located in administrative territory
  # https://www.wikidata.org/wiki/Property:P131
  ?city wdt:P131* ?region.
  # label of the City
  ?city rdfs:label ?cityLabel filter (lang(?cityLabel) = "en").
  # instance of human settlement https://www.wikidata.org/wiki/Q486972
  ?city wdt:P31/wdt:P279* wd:Q486972 .
  # geoName Identifier
  ?city wdt:P1566 ?geoNameId.
  # population of city
  OPTIONAL { ?city wdt:P1082 ?cityPop.}
   # get the coordinates
  OPTIONAL { 
      ?city wdt:P625 ?cityCoord.
  } 
} 
ORDER BY ?cityLabel""" % values
        wd=SPARQL(self.endpoint)
        results=wd.query(queryString)
        cityList=wd.asListOfDicts(results)
        return cityList
                
        
    def getCountries(self):
        '''
        get a list of countries
        
        `try query <https://query.wikidata.org/#%23%20get%20a%20list%20of%20countries%0A%23%20for%20geograpy3%20library%0A%23%20see%20https%3A%2F%2Fgithub.com%2Fsomnathrakshit%2Fgeograpy3%2Fissues%2F15%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20wd%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX%20wdt%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX%20p%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2F%3E%0APREFIX%20ps%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fstatement%2F%3E%0APREFIX%20pq%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fqualifier%2F%3E%0A%23%20get%20City%20details%20with%20Country%0ASELECT%20DISTINCT%20%3Fcountry%20%3FcountryLabel%20%3FcountryIsoCode%20%3FcountryPopulation%20%3FcountryGDP_perCapita%20%3Fcoord%20%20WHERE%20%7B%0A%20%20%23%20instance%20of%20City%20Country%0A%20%20%3Fcountry%20wdt%3AP31%2Fwdt%3AP279%2a%20wd%3AQ3624078%20.%0A%20%20%23%20label%20for%20the%20country%0A%20%20%3Fcountry%20rdfs%3Alabel%20%3FcountryLabel%20filter%20%28lang%28%3FcountryLabel%29%20%3D%20%22en%22%29.%0A%20%20%23%20get%20the%20coordinates%0A%20%20%3Fcountry%20wdt%3AP625%20%3Fcoord.%0A%20%20%23%20https%3A%2F%2Fwww.wikidata.org%2Fwiki%2FProperty%3AP297%20ISO%203166-1%20alpha-2%20code%0A%20%20%3Fcountry%20wdt%3AP297%20%3FcountryIsoCode.%0A%20%20%23%20population%20of%20country%0A%20%20%3Fcountry%20wdt%3AP1082%20%3FcountryPopulation.%0A%20%20%23%20https%3A%2F%2Fwww.wikidata.org%2Fwiki%2FProperty%3AP2132%0A%20%20%23%20nonminal%20GDP%20per%20capita%0A%20%20%3Fcountry%20wdt%3AP2132%20%3FcountryGDP_perCapita.%0A%7D>`_
      
        '''
        queryString="""# get a list of countries
# for geograpy3 library
# see https://github.com/somnathrakshit/geograpy3/issues/15
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
# get City details with Country
SELECT DISTINCT ?country ?countryLabel ?countryIsoCode  ?countryCoord  ?countryPopulation ?continent ?continentLabel
WHERE {
  # instance of Country
  ?country wdt:P31/wdt:P279* wd:Q6256 .
  # VALUES ?country { wd:Q55}.
  # label for the country
  ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en").
  # get the continent (s)
  #OPTIONAL {
  #  ?country wdt:P30 ?continent.
  #  ?continent rdfs:label ?continentLabel filter (lang(?continentLabel) = "en").
  #}
  # get the coordinates
  OPTIONAL { 
      ?country wdt:P625 ?countryCoord.
  } 
  # https://www.wikidata.org/wiki/Property:P297 ISO 3166-1 alpha-2 code
  ?country wdt:P297 ?countryIsoCode.
  # population of country   
  OPTIONAL
  { 
    SELECT ?country (max(?countryPopulationValue) as ?countryPopulation)
    WHERE {
      ?country wdt:P1082 ?countryPopulationValue
    } group by ?country
  }
  # https://www.wikidata.org/wiki/Property:P2132
  # nominal GDP per capita
  # OPTIONAL { ?country wdt:P2132 ?countryGDP_perCapitaValue. }
}
ORDER BY ?countryIsoCode"""
        wd=SPARQL(self.endpoint)
        results=wd.query(queryString)
        self.countryList=wd.asListOfDicts(results)

    def getRegions(self):
        '''
        get Regions from Wikidata
        
        `try query <https://query.wikidata.org/#%23%20get%20a%20list%20of%20regions%0A%23%20for%20geograpy3%20library%0A%23%20see%20https%3A%2F%2Fgithub.com%2Fsomnathrakshit%2Fgeograpy3%2Fissues%2F15%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20wd%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX%20wdt%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX%20wikibase%3A%20%3Chttp%3A%2F%2Fwikiba.se%2Fontology%23%3E%0ASELECT%20%3Fcountry%20%3FcountryLabel%20%3FcountryIsoCode%20%3Fregion%20%3FregionIsoCode%20%3FregionLabel%20%3Fpopulation%20%3Flocation%0AWHERE%0A%7B%0A%20%20%23%20administrative%20unit%20of%20first%20order%0A%20%20%3Fregion%20wdt%3AP31%2Fwdt%3AP279%2a%20wd%3AQ10864048.%0A%20%20OPTIONAL%20%7B%0A%20%20%20%20%20%3Fregion%20rdfs%3Alabel%20%3FregionLabel%20filter%20%28lang%28%3FregionLabel%29%20%3D%20%22en%22%29.%0A%20%20%7D%0A%20%20%23%20filter%20historic%20regions%0A%20%20%23%20FILTER%20NOT%20EXISTS%20%7B%3Fregion%20wdt%3AP576%20%3Fend%7D%0A%20%20%23%20get%20the%20population%0A%20%20%23%20https%3A%2F%2Fwww.wikidata.org%2Fwiki%2FProperty%3AP1082%0A%20%20OPTIONAL%20%7B%20%3Fregion%20wdt%3AP1082%20%3Fpopulation.%20%7D%0A%20%20%23%20%23%20https%3A%2F%2Fwww.wikidata.org%2Fwiki%2FProperty%3AP297%0A%20%20OPTIONAL%20%7B%20%0A%20%20%20%20%3Fregion%20wdt%3AP17%20%3Fcountry.%0A%20%20%20%20%23%20label%20for%20the%20country%0A%20%20%20%20%3Fcountry%20rdfs%3Alabel%20%3FcountryLabel%20filter%20%28lang%28%3FcountryLabel%29%20%3D%20%22en%22%29.%0A%20%20%20%20%3Fcountry%20wdt%3AP297%20%3FcountryIsoCode.%20%0A%20%20%7D%0A%20%20%23%20isocode%20state%2Fprovince%0A%20%20%3Fregion%20wdt%3AP300%20%3FregionIsoCode.%0A%20%20%23%20https%3A%2F%2Fwww.wikidata.org%2Fwiki%2FProperty%3AP625%0A%20%20OPTIONAL%20%7B%20%3Fregion%20wdt%3AP625%20%3Flocation.%20%7D%0A%7D>`_
        '''
        queryString="""# get a list of regions
# for geograpy3 library
# see https://github.com/somnathrakshit/geograpy3/issues/15
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT DISTINCT ?country ?countryLabel ?countryIsoCode ?region ?regionLabel ?regionIsoCode ?regionPopulation ?location
WHERE
{
  # administrative unit of first order
  ?region wdt:P31/wdt:P279* wd:Q10864048.
  OPTIONAL {
     ?region rdfs:label ?regionLabel filter (lang(?regionLabel) = "en").
  }
  # isocode state/province (mandatory - filters historic regions while at it ...)
  # filter historic regions
  # FILTER NOT EXISTS {?region wdt:P576 ?end}
  { 
    SELECT ?region (max(?regionAlpha2) as ?regionIsoCode) (max(?regionPopulationValue) as ?regionPopulation) (max(?locationValue) as ?location)
    WHERE {
      ?region wdt:P300 ?regionAlpha2.
      # get the population
      # https://www.wikidata.org/wiki/Property:P1082
      OPTIONAL {
        ?region wdt:P1082 ?regionPopulationValue
      } 
      # get he location
      # https://www.wikidata.org/wiki/Property:P625
      OPTIONAL {
        ?region wdt:P625 ?locationValue. 
       }
    } GROUP BY ?region
  }
  # # https://www.wikidata.org/wiki/Property:P297
  OPTIONAL { 
    ?region wdt:P17 ?country.
    # label for the country
    ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en").
    ?country wdt:P297 ?countryIsoCode. 
  }
} ORDER BY ?regionIsoCode"""
        wd=SPARQL(self.endpoint)
        results=wd.query(queryString)
        self.regionList=wd.asListOfDicts(results)

    def getCitiesOfRegion(self, regionWikidataId: str, limit:int):
        """
        Queries the cities of the given region. If the region is a city state the region is returned as city.
        The cities are ordered by population and can be limited by the given limit attribute.

        Args:
            regionWikidataId: wikidata id of the region the cities should be queried for
            limit: Limits the amount of returned cities

        Returns:
            Returns list of cities of the given region ordered by population
        """
        query = """
SELECT distinct ?city ?cityLabel ?cityPop ?cityCoord
WHERE {
  VALUES ?possibleCityID {wd:Q1549591 wd:Q515 wd:Q1637706 wd:Q1093829 wd:Q486972}
  wd:%s  (^wdt:P131|^wdt:P131/^wdt:P131|^wdt:P131/^wdt:P131/^wdt:P131|^wdt:P131/^wdt:P131/^wdt:P131/^wdt:P131) ?city .
  {
    ?city wdt:P31 ?x .
    ?x wdt:P279 ?possibleCityID .
  }UNION{
    ?city wdt:P31 ?possibleCityID .
  }
  OPTIONAL{
     ?city rdfs:label ?cityLabel .
    FILTER(lang(?cityLabel)="en")
  }
  OPTIONAL{
     ?city wdt:P1082 ?cityPop .
  }
  OPTIONAL{
     ?city wdt:P625 ?cityCoord .
  }

}
ORDER BY DESC(?cityPop)
LIMIT %s
    """ % (regionWikidataId, limit)
        askIfCity = """
SELECT *
WHERE{
  VALUES ?possibleCityID {wd:Q1549591 wd:Q515 wd:Q1637706 wd:Q1093829 wd:Q486972 wd:Q133442}
  wd:%s  wdt:P31 ?possibleCityID .
}
    """ % (regionWikidataId)
        wd = SPARQL(self.endpoint)
        cities = []
        ids = []
        # check if region is city (city-state)
        try:
            isCityResult = wd.query(askIfCity)
            isCity = wd.asListOfDicts(isCityResult)
            if isCity:
                # TODO: return region as city once city class is refactored
                pass
            else:
                pass
        except Exception as e:
            print(e)
            pass

        try:
            queryRes = wd.query(query)
            cityLoD=wd.asListOfDicts(queryRes)
            res=[]
            # [{'city': 'http://www.wikidata.org/entity/Q1050826', 'citylabel': 'Greater Los Angeles Area', 'population': 18550288.0, 'coordinates': 'Point(-118.25 35.05694444)'}]
            for cityRecord in cityLoD:
                res.append(cityRecord)
            return res
        except Exception as  e:
            print(e)
            pass
        return cities

    @staticmethod
    def getCoordinateComponents(coordinate:str) -> (float, float):
        '''
        Converts the wikidata coordinate representation into its subcomponents longitude and latitude
        Example: 'Point(-118.25 35.05694444)' results in ('-118.25' '35.05694444')

        Args:
            coordinate: coordinate value in the format as returned by wikidata queries

        Returns:
            Returns the longitude and latitude of the given coordinate as separate values
        '''
        # https://stackoverflow.com/a/18237992/1497139
        floatRegex=r"[-+]?\d+([.,]\d*)?"
        regexp=fr"Point\((?P<lon>{floatRegex})\s+(?P<lat>{floatRegex})\)"
        cMatch=None
        if coordinate:
            try:
                cMatch = re.search(regexp, coordinate)
            except Exception as ex:
                # ignore
                pass
        if cMatch:
            latStr=cMatch.group("lat")
            lonStr=cMatch.group("lon")
            lat,lon=float(latStr.replace(",",".")),float(lonStr.replace(",","."))
            if lon>180:
                lon=lon-360
            return lat,lon
        else:
            # coordinate does not have the expected format
            return None, None

    @staticmethod
    def getWikidataId(wikidataURL:str):
        '''
        Extracts the wikidata id from the given wikidata URL

        Args:
            wikidataURL: wikidata URL the id should be extracted from

        Returns:
            The wikidata id if present in the given wikidata URL otherwise None
        '''

        # regex pattern taken from https://www.wikidata.org/wiki/Q43649390 and extended to also support property ids
        wikidataidMatch = re.search(r"[PQ][1-9]\d*", wikidataURL)
        if wikidataidMatch.group(0):
            wikidataid = wikidataidMatch.group(0)
            return wikidataid
        else:
            return None

    @staticmethod
    def getValuesClause(varName:str, values, wikidataEntities:bool=True):
        '''
        generates the SPARQL value clause for the given variable name containing the given values
        Args:
            varName: variable name for the ValuesClause
            values: values for the clause
            wikidataEntities(bool): if true the wikidata prefix is added to the values otherwise it is expected taht the given values are proper IRIs

        Returns:
            str
        '''
        clauseValues=""
        if isinstance(values, list):
            for value in values:
                if wikidataEntities:
                    clauseValues+=f"wd:{value} "
                else:
                    clauseValues+=f"{value} "
        else:
            if wikidataEntities:
                clauseValues = f"wd:{values} "
            else:
                clauseValues = f"{values} "
        clause = "VALUES ?%s { %s }" %(varName, clauseValues)
        return clause