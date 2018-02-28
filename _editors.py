sql = """SELECT * FROM krimisiden._editors;"""

rdfcmds = """
try:
    subject = URIRef("http://krimisiden.dk/content.php?page=editor&value=" + str(row['username']))
    self.graph.add( (subject, RDF.type, SCHEMA['Person'] )) 
    if row['description']: self.graph.add( (subject, SCHEMA['description'], Literal(row['description'])))
    if row['username']: self.graph.add( (subject, SCHEMA['additionalName'], Literal(row['username'])))
    if row['name']: self.graph.add( (subject, SCHEMA['name'], Literal(row['name'])))
    if row['familyname']: self.graph.add( (subject, SCHEMA['familyName'], Literal(row['familyname'])))
    if row['givenname']: self.graph.add( (subject, SCHEMA['givenName'], Literal(row['givenname'])))
    if row['viafid']: self.graph.add( (subject, SCHEMA['sameAs'],  URIRef("https://viaf.org/viaf/" + str(row['viafid']))))
    self.graph.add( (subject, SCHEMA['additionalType'], URIRef('http://xmlns.com/foaf/0.1/Person') ) )

except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    print(sys.exc_info()[2])
    print(sys.exc_info()[2].tb_lineno)
"""
