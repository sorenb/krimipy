sql = """
SELECT krimisiden.articles.tableid,
createddate,
title,
teaser,
content,
givenname,
familyname,
krimisiden.articles.username
from krimisiden.articles
left join krimisiden._editors on krimisiden._editors.username = krimisiden.articles.username
;
"""

rdfcmds = """
# datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%Y%m%d %H:%M:%S').isoformat()
# datotid = datetime.datetime.now(pytz.timezone('Europe/Paris')).isoformat()

# Pythons version of ternary operator... 
datotid = pytz.utc.localize(datetime.datetime.utcfromtimestamp( int(row['createddate']) )).astimezone(pytz.timezone("Europe/Copenhagen") ).isoformat() if row['createddate'] else ''
titel = row['title'] if row['title'] else ''
# typen = row['lit_type'] if row['lit_type'] else ''
fornavn = row['givenname'] if row['givenname'] else ''
efternavn = row['familyname'] if row['familyname'] else ''
# dato = ". - , " + str(row['orgyear']) + " (dansk udgivelsesår)" if row['orgyear'] else ''
#author = fornavn + ' ' + efternavn

#headline = titel + ' af ' + fornavn + ' ' + efternavn + dato
#headline = titel + ' : ' + typen + ' af ' + fornavn + ' ' + efternavn + dato

subject = URIRef("http://krimisiden.dk/content.php?page=article&value=" + str(row['tableid']))
if row['username']: self.graph.add( (subject, SCHEMA['author'], URIRef("http://krimisiden.dk/content.php?page=editor&value=" + str(row['username'])) ))
self.graph.add( (subject, RDF.type, SCHEMA['Article'] )) 
self.graph.add( (subject, SCHEMA['url'], subject )) 
# self.graph.add( (subject, SCHEMA['headline'], Literal(headline)) )
if row['title']: self.graph.add( (subject, SCHEMA['title'], Literal(row['title'])))
#self.graph.add( (subject, SCHEMA['author'], Literal(author) )) 
self.graph.add( (subject, SCHEMA['datePublished'], Literal(str(datotid), datatype=XSD.dateTime ))) 
# TODO keywords forefindes ikke pt. i datasættet (det er pt. tekstrenge i content på nogle få articles der starter med #)
if row['content']: self.graph.add( (subject, SCHEMA['articleBody'], Literal(row['content'])))
self.graph.add( (subject, SCHEMA['additionalType'], URIRef("http://id.loc.gov/ontologies/bibframe.html#c_Text")) )
if row['teaser']: self.graph.add( (subject, SCHEMA['articleDescription'], Literal(row['teaser'])) )
"""
