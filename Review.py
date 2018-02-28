sql = """SELECT krimisiden.bookreview.tableid bookreview_id,
dktitle,
firstname,
lastname,
orgyear,
krimisiden.bookreview.bookindex,
krimisiden.bookreview.teaser description,
krimisiden.bookreview."content" reviewbody,
krimisiden.bookreview.username author,
krimisiden.bookreview.createddate,
krimisiden.bookstars.stars reviewrating,
krimisiden.books."type" lit_type
from krimisiden.bookreview
left join krimisiden.books on krimisiden.books.tableid = krimisiden.bookreview.bookindex
left join krimisiden.bookstars on krimisiden.bookstars.bookindex = krimisiden.bookreview.bookindex
left join krimisiden.bookauthors on krimisiden.bookauthors.bookindex = krimisiden.books.tableid
left join krimisiden.authors on krimisiden.authors.tableid = krimisiden.bookauthors.authorindex
left join krimisiden.names on krimisiden.names.authorindex = krimisiden.authors.tableid
where krimisiden.books.krimishow = 1
order by bookindex
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=bookreview&value=" + str(row['bookreview_id']))

# Pythons version of ternary operator... 
datotid = pytz.utc.localize(datetime.datetime.utcfromtimestamp( int(row['createddate']) )).astimezone(pytz.timezone("Europe/Copenhagen") ).isoformat() if row['createddate'] else ''
titel = row['dktitle'] if row['dktitle'] else ''
typen = row['lit_type'] if row['lit_type'] else ''
fornavn = row['firstname'] if row['firstname'] else ''
efternavn = row['lastname'] if row['lastname'] else ''
dato = ". - , " + str(row['orgyear']) + " (dansk udgivelsesår)" if row['orgyear'] else ''

headline = titel + ' : ' + typen + ' af ' + fornavn + ' ' + efternavn + dato

self.graph.add( (subject, RDF.type, SCHEMA['Review'] )) 
self.graph.add( (subject, SCHEMA['url'], subject )) 
self.graph.add( (subject, SCHEMA['headline'], Literal(headline)) )
self.graph.add( (subject, SCHEMA['author'], Literal(row['author']) )) 
self.graph.add( (subject, SCHEMA['datePublished'], Literal(str(datotid), datatype=XSD.dateTime ))) 
# TODO keywords forefindes ikke pt. i datasættet (det er pt. tekstrenge i content på nogle få articles der starter med #)
if row['reviewbody']: self.graph.add( (subject, SCHEMA['reviewBody'], Literal(row['reviewbody'])))
self.graph.add( (subject, SCHEMA['additionalType'], URIRef("http://id.loc.gov/ontologies/bibframe.html#c_Text")) )
self.graph.add( (subject, SCHEMA['itemReviewed'], URIRef("http://krimisiden.dk/content.php?page=book&value=" + str(row['bookindex']))) )
self.graph.add( (subject, SCHEMA['reviewRating'], Literal(str(row['reviewrating'] ))))
self.graph.add( (subject, SCHEMA['image'],  URIRef("http://krimisiden.dk/covers/" + str(row['bookindex']) + ".jpg")))
"""
