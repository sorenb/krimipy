sql = """
SELECT krimisiden.town.tableid,
krimisiden.town."name",
krimisiden.country2."name" containedinplace,
krimisiden.country2.tableid country_id,
krimisiden._wikidata_city_openrefine.wikidata
from krimisiden.town
left join krimisiden.country2 on krimisiden.country2.tableid = krimisiden.town.countryindex
left join krimisiden._wikidata_city_openrefine on krimisiden._wikidata_city_openrefine.tableid = krimisiden.town.tableid
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=city&value=" + str(row['tableid']))
self.graph.add( (subject, RDF.type, SCHEMA['City'] )) 
if row['name']: self.graph.add( (subject, SCHEMA['name'], Literal(row['name'])))
if row['country_id']: self.graph.add( (subject, SCHEMA['containedInPlace'],  URIRef("http://krimisiden.dk/content.php?page=country&value=" + str(row['country_id']))) )
if row['containedinplace']: self.graph.add( (subject, SCHEMA['containedInPlace'],  Literal(row['containedinplace'])) )
if row['tableid']: self.graph.add( (subject, SCHEMA['identifier'], URIRef("http://krimisiden.dk/content.php?page=city&value=" + str(row['tableid']))) )
if row['wikidata']: self.graph.add( (subject, SCHEMA['sameAs'], Literal(row['wikidata']) ) ) 
"""
