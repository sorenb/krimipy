sql = """
SELECT  krimisiden.books.tableid,
dktitle krimisiden_title,
firstname || ' ' || lastname author_string,
authors.tableid author_id,
txtif.title txtif_title,
orgtitle,
CASE WHEN username = 'PKFredborg' THEN 'Per: '||teaser
WHEN username = 'nanna' THEN 'Nanna: '||teaser
WHEN username = 'Loneha' THEN 'Lone: '||teaser
WHEN username = 'mha' THEN 'Marit: '||teaser
WHEN username = 'bogh' THEN 'Susanne: '||teaser
WHEN username = 'sof' THEN 'Sofie: '||teaser
ELSE username||': '||teaser
END description,
isn isbn,
txtif.key faust,
orgyear,
txtif.author,
krimisiden.bookauthors.authorindex,
fullname,
firstname,
lastname,
krimisiden.bookmaincharacter.maincharacterindex,
krimisiden.genre.name genre,
krimisiden.genre.tableid genre_id,
krimisiden.series.title series_title,
krimisiden.booktown.townindex town_id
from krimisiden.books
left join txtif on txtif.title = krimisiden.books.dktitle
left join krimisiden.bookauthors on krimisiden.bookauthors.bookindex = krimisiden.books.tableid
left join krimisiden.authors on krimisiden.authors.tableid = krimisiden.bookauthors.authorindex
left join krimisiden.names on krimisiden.names.authorindex = krimisiden.authors.tableid
left join krimisiden.bookgenre on krimisiden.bookgenre.bookindex = krimisiden.books.tableid
left join krimisiden.genre on krimisiden.genre.tableid = krimisiden.bookgenre.genreindex
left join krimisiden.bookseries on krimisiden.bookseries.bookindex = krimisiden.books.tableid
left join krimisiden.series on krimisiden.series.tableid = krimisiden.bookseries.seriesindex
left join krimisiden.bookreview on krimisiden.bookreview.bookindex = krimisiden.books.tableid
left join krimisiden.booktown on krimisiden.booktown.bookindex = krimisiden.books.tableid
left join krimisiden.bookmaincharacter on krimisiden.bookmaincharacter.bookindex = krimisiden.books.tableid
where krimisiden.books.krimishow = 1
and txtif.author ilike '%' || lastname || '%'
;
"""

rdfcmds = """
subject = URIRef("http://krimisiden.dk/content.php?page=book&value=" + str(row['tableid']))
self.graph.add( (subject, RDF.type, SCHEMA['Book'] )) 
if row['krimisiden_title']: self.graph.add( (subject, SCHEMA['name'], Literal(row['krimisiden_title'])))
if row['author_string']: self.graph.add( (subject, SCHEMA['author'], Literal(row['author_string'])))
if row['author_id']: self.graph.add( (subject, SCHEMA['author'],  URIRef("http://krimisiden.dk/content.php?page=author&value=" + str(row['author_id']))) )
if row['maincharacterindex']: self.graph.add( (subject, SCHEMA['character'],  URIRef("http://krimisiden.dk/content.php?page=person&value=" + str(row['maincharacterindex']))) )
if row['author_string']: self.graph.add( (subject, SCHEMA['mainCharacter'], Literal(row['author_string'])))
if row['orgyear']: self.graph.add( (subject, SCHEMA['datePublished'], Literal(row['orgyear'], datatype=XSD.gYear ))) 
if row['genre_id']: self.graph.add( (subject, SCHEMA['genre'], URIRef("http://krimisiden.dk/content.php?page=genre&value=" + str(row['genre_id']))) )
#if row['genre']: self.graph.add( (subject, SCHEMA['genre'], Literal(row['genre'])))
if row['series_title']: self.graph.add( (subject, SCHEMA['isPartOf'], Literal(row['series_title'])))
if row['description']: self.graph.add( (subject, SCHEMA['description'], Literal(row['description'])))
if row['isbn']: self.graph.add( (subject, SCHEMA['isbn'], Literal(row['isbn'])))
if row['faust']: self.graph.add( (subject, SCHEMA['productID'], Literal("faust:" + str(row['faust']))))
if row['town_id']: self.graph.add( (subject, SCHEMA['contentLocation'], URIRef("http://krimisiden.dk/content.php?page=city&value=" + str(row['town_id']))) )
self.graph.add( (subject, SCHEMA['identifier'], URIRef("http://krimisiden.dk/content.php?page=book&value=" + str(row['tableid']))) )
self.graph.add( (subject, SCHEMA['additionalType'], URIRef("http://id.loc.gov/ontologies/bibframe.html#c_Text")) )
self.graph.add( (subject, SCHEMA['image'],  URIRef("http://krimisiden.dk/covers/" + str(row['tableid']) + ".jpg")))
"""
