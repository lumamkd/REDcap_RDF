#!/usr/bin/env python

from config import config
import requests
import json
import pprint
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import DC, FOAF, DCTERMS

# Create a Graph
g = Graph()

AHRIRedcap = Namespace("ttps://population.ahri.org/redcap_v14.0.17/")
AHRIRedcapRecord = Namespace("https://population.ahri.org/redcap_v14.0.17/record/")
SIO = Namespace("http://semanticscience.org/resource/")

fields = {
    'token': config['api_token'],
    'content': 'record',
    'format': 'json',
    'type': 'flat'
}

r = requests.post(config['api_url'],data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.text)

results = json.loads(r.text)
#pprint.pprint(results)
print(len(results))

for row in results:
    g.add((AHRIRedcap[row['record_id']], RDF.type, SIO["000088"]))
    for key, value in row.items():
        if value:  # Check if the value is not empty
            g.add((AHRIRedcapRecord[row['record_id']], AHRIRedcap[key], Literal(value)))

        if row['redcap_repeat_instrument'] != '':
            g.add((AHRIRedcap[key], RDFS.label, Literal(key)))
            g.add((AHRIRedcap[key], DCTERMS.isPartOf, AHRIRedcap[row["redcap_repeat_instrument"]]))

print(g.serialize(destination="firstRC.ttl", format="turtle"))