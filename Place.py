sql = """
SELECT krimisiden._continent_slash_place_viaf.*, 
krimisiden.country2.tableid country_id
from krimisiden._continent_slash_place_viaf
left join krimisiden.country2 on krimisiden.country2.continentindex = krimisiden._continent_slash_place_viaf.tableid
;
"""

rdfcmds = """
# We only want to try and add nodes that actually have a url as subject, and since
# krimisiden does not have urls representing continent/place we use wikidata, but
# wikidata could in theory be missing we use wikidata, but
# wikidata could in theory be missing..
if row['wikidata']: 
  # subject = Literal(row['name']) # using a literal here is seemingly not accepted by fuseki/jena (or is it an encoding issue with danish characters?)
  subject = URIRef("https://www.wikidata.org/wiki/" + str(row['wikidata']))
  self.graph.add( (subject, RDF.type, SCHEMA['Place'] ) )
  if row['name']: self.graph.add( (subject, SCHEMA['name'], Literal(row['name'])))
  if row['country_id']: self.graph.add( (subject, SCHEMA['containsPlace'], URIRef("http://krimisiden.dk/content.php?page=country&value=" + str(row['country_id'])) ) )
  if row['viaf']: self.graph.add( (subject, SCHEMA['sameAs'], URIRef("https://viaf.org/viaf/" + str(row['viaf'])) ) )
  #if row['wikidata']: self.graph.add( (subject, SCHEMA['sameAs'], URIRef("https://www.wikidata.org/wiki/" + str(row['wikidata'])) ) )
"""
