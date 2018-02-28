sql = """
select 'https://www.odensebib.dk/sites/www.odensebib.dk/files/' || md5(name) || '.jpg' identifier, 'http://krimisiden.dk/content.php?page=genre&value=' || tableid about from krimisiden.genre where site = 'krimi'
union all
select 'http://krimisiden.dk/covers/' || tableid || '.jpg' identifier, 'http://krimisiden.dk/content.php?page=book&value=' || books.tableid about from krimisiden.books where krimisiden.books.krimishow = 1
;
"""

rdfcmds = """
subject = URIRef( str(row['identifier']) )
self.graph.add( (subject, RDF.type, SCHEMA['ImageObject'] ))
if row['identifier']: self.graph.add( (subject, SCHEMA['identifier'], URIRef(row['identifier'])) )
if row['about']: self.graph.add( (subject, SCHEMA['about'], URIRef(row['about'])) )
#if row['creator']: self.graph.add( (subject, SCHEMA['creator'], Literal(row['creator'])))
"""
