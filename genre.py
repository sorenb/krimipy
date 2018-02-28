sql = "SELECT tableid, name, shortdescription, description FROM krimisiden.genre where site = 'krimi';"

rdfcmds = """
subject = URIRef('http://krimisiden.dk/content.php?page=genre&value=' + str(row['tableid']))
self.graph.add( (subject, RDF.type, SCHEMA['genre'] ))
if row['tableid']: self.graph.add( (subject, SCHEMA['url'], URIRef('http://krimisiden.dk/content.php?page=genre&value=' + str(row['tableid']))) )
if row['name']: self.graph.add( (subject, SCHEMA['name'], Literal(row['name'])))
if row['shortdescription']: self.graph.add( (subject, SCHEMA['disambiguatingDescription'], Literal(row['shortdescription'])))
if row['description']: self.graph.add( (subject, SCHEMA['description'], Literal(row['description'])))
"""
