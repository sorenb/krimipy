#!/usr/bin/python3

import os
import sys
import datetime
import pytz # timezone stuff
import requests
import psycopg2
import psycopg2.extras
import argparse
import subprocess
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, plugin
from rdflib.namespace import RDF

class Converter:

    def __init__( self,conn,endpoint ):
        self.conn = conn
        self.cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.graph = Graph()
        self.graphname = None
        self.url = endpoint #  + '/' + self.dataset 
   
    def addtotriplestore( self ):
        """Function to add graph to a triple store"""
        print ('\n--- Posting ' + self.graphname + ' triples to triple store at ' + self.url + ' :  ', end='')
        headers = {"Content-Type": "text/turtle;charset=utf-8"}
        response = requests.post(self.url, data=self.graph.serialize(format='turtle'), headers=headers)
        print (response)

    def delete( self,deletetype ):
        """Function to delete rdf types from a triple store"""
        print ('\n--- DELETING ' + deletetype + ' triples from triple store at ' + self.url + '! :  ', end='')
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        data = "update=PREFIX+schema:+<http://schema.org/>+DELETE+{?s+?p+?o}+WHERE+{?s+?pr+" + deletetype +  ".+?s+?p+?o}"
        response = requests.post(self.url + "/update", data, headers=headers)
        print (response)

    def extract( self,sql,rdfcmds,graphname ):
        """Function to extract each line and convert it to triples"""
        SCHEMA = Namespace('http://schema.org/') # use schema as prefix for http://schema.org
        XSD = Namespace('http://www.w3.org/2001/XMLSchema#') # xsd namespace for datatypes 
        self.graphname = graphname
        self.graph.bind('schema', SCHEMA) 
        self.graph.bind('xsd', XSD) 
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
        except:
            e = sys.exc_info()[0]
            print( "Exception occured with SQL commands: %s" % e )
            self.graph = None
        try:
            for row in rows:
                exec(rdfcmds)
            self.addtotriplestore()
        except Exception as inst:
            e = sys.exc_info()[0]
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
            print(sys.exc_info()[2].tb_lineno)
            print( "Exception occured with RDF commands: %s: " % e, end='' )
            print(inst)          # __str__ allows args to be printed directly,            
            self.graph = None

    def writetofile( self, rdfformat ):
        """Function to write graph to file"""
        print (' |__ writing ' + self.graphname + ' triples to file ' + self.graphname + '.' + rdfformat )

        if rdfformat != 'hdt':
            context = {"@vocab": "http://schema.org", "@language": "da"}
            fp = open( self.graphname + '.' + rdfformat,'wb' )
            fp.write( self.graph.serialize(format=rdfformat, context=context, indent=4) )
            fp.close()

        else:
            tmpfile = self.graphname + '.nt'
            hdtfile = self.graphname + '.' + rdfformat
            fp = open( tmpfile,'wb' )
            fp.write( self.graph.serialize(format='nt') )
            fp.close()
            subprocess.call(["rdf2hdt", tmpfile, hdtfile])


def main():

    parser = argparse.ArgumentParser()
   
    # Mutual exclusivity needed between insert and delete functionality arguments:
    exgroup = parser.add_mutually_exclusive_group()

    exgroup.add_argument('-d','--delete',
                        action='store_true',
                        dest='delete',
                        help='SPARQL endpoint URL to delete triples from, e.g. http://example.com:3030/datasetname')
 
    parser.add_argument('-e','--endpoint',
                        action='store',
                        dest='endpoint',
                        help='SPARQL endpoint URL to send triples to, e.g. http://example.com:3030/datasetname')

    exgroup.add_argument('-f','--fileformat',
                        action='store',
                        dest='fileformat',
                        help='Store triples in a local file of the specified format')

    # RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, RDFa, Microdata, HDT.
    # xml, json-ld, hdt, ttl, N3, NTriples, N-Quads, Turtle, TriX, RDFa, Microdata

    parser.add_argument('posparms', nargs='*')
    
    arguments = parser.parse_args()

    # Postgres connection string. Requires import from a password file in the homedir of 
    # the user running this script. It must be called .postpass.py and contain vars like these:

    # dbname = "database"
    # user = "database_user"
    # host = "192.168.192.168"
    # password = "password"

    exec( open(os.getenv("HOME") + "/.postpass.py").read(),globals() )
    constring = "dbname=" + dbname + " user=" + user + " host=" + host + " password=" + password
    
    # Create connection to database
    try:
        conn=psycopg2.connect(constring)
    
    except Exception as excep: 
        print( excep )
        print ("I am unable to connect to the database.")
    
    for i in range(len(arguments.posparms)):
        
        # Did the user set the -d/--delete option?
        if arguments.delete:

            # Here posparms are schema.org types to delete
            deletetype = str(arguments.posparms[i])
            convtr = Converter( conn,arguments.endpoint )
            convtr.delete(deletetype)

        else:

            # Here posparms are names of files with sql and rdflib commands 
            exec(open(arguments.posparms[i]).read(),globals())
 
            graphname = str(arguments.posparms[i]).replace('.py','')
            convtr = Converter( conn,arguments.endpoint )
            convtr.extract( sql,rdfcmds,graphname ) # The first two vars here are read from the file
            convtr.writetofile( arguments.fileformat )

    print('\n')

if __name__ == "__main__":
    main()
