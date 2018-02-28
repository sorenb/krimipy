sql = """
SELECT krimisiden.series.tableid series_id,
krimisiden.series.title,
krimisiden.books.tableid books_id,
krimisiden.books.dktitle
from krimisiden.series
right join krimisiden.bookseries on krimisiden.bookseries.seriesindex = krimisiden.series.tableid
right join krimisiden.books on krimisiden.books.tableid = krimisiden.bookseries.bookindex
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=series&value=" + str(row['series_id']))
self.graph.add( (subject, RDF.type, SCHEMA['Series'] )) 
if row['title']: self.graph.add( (subject, SCHEMA['name'], Literal(row['title'])))
if row['series_id']: self.graph.add( (subject, SCHEMA['identifier'], URIRef("http://krimisiden.dk/content.php?page=series&value=" + str(row['series_id']))) )
if row['books_id']: self.graph.add( (subject, SCHEMA['hasPart'], URIRef("http://krimisiden.dk/content.php?page=book&value=" + str(row['books_id']))) )
self.graph.add( (subject, SCHEMA['additionalType'], URIRef("http://id.loc.gov/ontologies/bibframe.html#p_seriesOf")) )
#if row['wikidata']: self.graph.add( (subject, SCHEMA['sameAs'], Literal(row['wikidata']) ) ) 
"""
