sql = """
SELECT krimisiden.country2.tableid,
krimisiden.country2."name"
from krimisiden.country2
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=country&value=" + str(row['tableid']))
self.graph.add( (subject, RDF.type, SCHEMA['Country'] ))
if row['name']: self.graph.add( (subject, SCHEMA['name'], Literal(row['name'])))
#if row['containinplace']: self.graph.add( (subject, SCHEMA['containInPlace'],  Literal(row['containedinplace'])) )
if row['tableid']: self.graph.add( (subject, SCHEMA['identifier'], URIRef("http://krimisiden.dk/content.php?page=country&value=" + str(row['tableid']))) )
#if row['wikidata']: self.graph.add( (subject, SCHEMA['sameAs'], Literal(row['wikidata']) ) )
"""
