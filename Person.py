sql = """SELECT * FROM krimisiden.maincharacter WHERE site = 'krimi';"""

rdfcmds = """
try:
    # Pythons version of ternary operator... 
    fornavn = row['firstname'] if row['firstname'] else ''
    efternavn = row['lastname'] if row['lastname'] else ''
    fullname = str(fornavn).strip() + ' ' + str(efternavn).strip() if row['firstname'] and row['lastname'] else str(fornavn) + str(efternavn)
   
    # print(fullname) 
    # if row['firstname'] and row['lastname']:
    #     fullname = fornavn.strip() + ' ' + efternavn.strip()
    # else:
    #     fullname = str(fornavn) + str(efternavn)

    subject = URIRef("http://krimisiden.dk/content.php?page=person&value=" + str(row['tableid']))
    self.graph.add( (subject, RDF.type, SCHEMA['Person'] )) 
    if fullname: self.graph.add( (subject, SCHEMA['name'], Literal(str(fullname)))) 
    if row['content']: self.graph.add( (subject, SCHEMA['description'], Literal(row['content'])))
    if row['lastname']: self.graph.add( (subject, SCHEMA['familyName'], Literal(row['lastname'])))
    if row['firstname']: self.graph.add( (subject, SCHEMA['givenName'], Literal(row['firstname'])))
    if row['job']: self.graph.add( (subject, SCHEMA['jobTitle'], Literal(row['job'])))
    self.graph.add( (subject, SCHEMA['identifier'],  URIRef("http://krimisiden.dk/content.php?page=person&value=" + str(row['tableid']))))
    self.graph.add( (subject, SCHEMA['additionalType'], URIRef('http://xmlns.com/foaf/0.1/Person') ) )

except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    print(sys.exc_info()[2])
    print(sys.exc_info()[2].tb_lineno)
"""
