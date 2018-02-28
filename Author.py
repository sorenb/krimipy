sql = """
select distinct
nullif(fullname,'') fullname,
nullif(krimidescription,'') krimidescription,
nullif(lastname,'') lastname,
nullif(firstname,'') firstname,
nullif(pseudonymnames,'') pseudonymnames,
nullif(realname,'') realname,
authors.tableid tableid,
viaf,
-- Aht. rdf-kommandoernes felter med integers, skal vi tjekke at der kun findes tal i flg. felter:
case when birthyear ~ '^[0-9]+$' then birthyear else NULL end birthyear,
case when birthmonth ~ '^[0-9]+$' then birthmonth else NULL end birthmonth,
case when birthday ~ '^[0-9]+$' then birthday else NULL end birthday,
case when deathyear ~ '^[0-9]+$' then deathyear else NULL end deathyear,
case when deathmonth ~ '^[0-9]+$' then deathmonth else NULL end deathmonth,
case when deathday ~ '^[0-9]+$' then deathday else NULL end deathday
from krimisiden._viaf_openrefine
left join krimisiden.authors on krimisiden.authors.tableid::bigint = krimisiden._viaf_openrefine.tableid::bigint
left join krimisiden.names on krimisiden.names.authorindex = krimisiden._viaf_openrefine.tableid::bigint
order by tableid
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=author&value=" + str(row['tableid']))
self.graph.add( (subject, RDF.type, SCHEMA['Person'] )) 

#datotid = pytz.utc.localize(datetime.datetime.utcfromtimestamp( int(row['createddate']) )).astimezone(pytz.timezone("Europe/Copenhagen") ).isoformat() if row['createddate'] else ''
#self.graph.add( (subject, SCHEMA['datePublished'], Literal(str(datotid), datatype=XSD.dateTime ))) 

if row['fullname']: self.graph.add( (subject, SCHEMA['name'], Literal(row['fullname'])))
if row['krimidescription']: self.graph.add( (subject, SCHEMA['description'], Literal(row['krimidescription'])))
if row['lastname']: self.graph.add( (subject, SCHEMA['familyName'], Literal(row['lastname'])))
if row['firstname']: self.graph.add( (subject, SCHEMA['givenName'], Literal(row['firstname'])))
if row['pseudonymnames']: self.graph.add( (subject, SCHEMA['additionalName'], Literal(row['pseudonymnames'])))
if row['realname']: self.graph.add( (subject, SCHEMA['additionalName'], Literal(row['realname'])))
self.graph.add( (subject, SCHEMA['identifier'],  URIRef("http://krimisiden.dk/content.php?page=author&value=" + str(row['tableid']))))
if row['viaf']: self.graph.add( (subject, SCHEMA['sameAs'], URIRef(row['viaf'])))
#if row['wikipedia']: self.graph.add( (subject, SCHEMA['sameAs'], URIRef(row['wikipedia'])) )
#if row['image']: self.graph.add( (subject, SCHEMA['image'], Literal(row['image'])) )
# self.graph.add( (subject, SCHEMA['image'], Literal('intetbillede.png')) ) TODO add images for 10 authors manually as examples
self.graph.add( (subject, SCHEMA['additionalType'], URIRef('http://bibfra.me/vocab/relation/author') ) )
self.graph.add( (subject, SCHEMA['additionalType'], URIRef('http://purl.org/dc/elements/1.1/creator') ) )
if (row['birthyear'] and row['birthmonth'] and row['birthday']): self.graph.add( (subject, SCHEMA['birthDate'], Literal(row['birthyear'] + '-' + '{:02}'.format(int(row['birthmonth'])) + '-' + '{:02}'.format(int(row['birthday'])), datatype=XSD.date) ) )
if (row['deathyear'] and row['deathmonth'] and row['deathday']): self.graph.add( (subject, SCHEMA['deathDate'], Literal(row['deathyear'] + '-' + '{:02}'.format(int(row['deathmonth'])) + '-' + '{:02}'.format(int(row['deathday'])), datatype=XSD.date) ) )
"""
