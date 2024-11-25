#!/usr/bin/env python

import requests
import json
import pprint
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS
from rdflib.namespace import DC, FOAF, DCTERMS

# Create a Graph
g = Graph()

AHRIRedcapURL = "https://population.ahri.org/api/"
AHRIRedcap = Namespace(AHRIRedcapURL)
AHRIRedcapRecord = Namespace("https://population.ahri.org/api/record/")
# SIO = Namespace("http://semanticscience.org/resource/")

fields = {
    'token': '1D6C6290BE8B3F190DCF6DC4BE679272',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}

r = requests.post(AHRIRedcapURL,data=fields)
print('HTTP Status: ' + str(r.status_code))
print(r.json())

results = r.json()
#pprint.pprint(results)
print(len(results))

for row in results:
    # g.add((AHRIRedcap[row['record_id']], RDF.type, SIO["000088"]))
    for key, value in row.items():
        if value:  # Check if the value is not empty
            g.add((AHRIRedcapRecord[row['record_id']], AHRIRedcap[key], Literal(value)))

        if row['redcap_repeat_instrument'] != '':
            g.add((AHRIRedcap[key], RDFS.label, Literal(key)))
            g.add((AHRIRedcap[key], DCTERMS.isPartOf, AHRIRedcap[row["redcap_repeat_instrument"]]))

print(g.serialize(destination="firstRC.ttl", format="turtle"))
