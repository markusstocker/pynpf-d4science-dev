# -*- coding: utf-8 -*-
import requests
import csv
from rdflib import Graph
from rdflib.plugins.sparql.results.csvresults import CSVResultSerializer
from io import BytesIO

globalvariables = None

with open('globalvariables.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    globalvariables = {rows[0]: rows[1] for rows in reader}

headers = {'Content-Type':'application/json',
           'Accept':'application/json',
           'gcube-token':globalvariables['gcube_token']}

res = requests.get('http://catalogue-ws.d4science.org/catalogue-ws/rest/api/items/show',
                   params={'id':'npfe_descriptions_at_hyytiaelae'},
                   headers=headers)
json = res.json()

g = Graph()

for resource in json['result']['resources']:
    g.parse(data=requests.get(resource['url']).content.decode('utf-8'), format="turtle")

q = """
SELECT ?beginning ?end ?classification ?place ?latitude ?longitude ?uri
WHERE {
?uri rdf:type lode:Event .
?uri lode:atTime ?atTime .
?atTime time:hasBeginning ?hasBeginning .
?hasBeginning time:inXSDDateTime ?beginning .
?atTime time:hasEnd ?hasEnd .
?hasEnd time:inXSDDateTime ?end .
?uri lode:atPlace ?atPlace .
?atPlace gn:name ?place .
?atPlace wgs84:lat ?latitude .
?atPlace wgs84:long ?longitude .
?uri smear:hasClassification ?hasClassification .
?hasClassification rdfs:label ?classification .
}
ORDER BY ASC(?beginning)
"""

serializer = CSVResultSerializer(g.query(q))
output = BytesIO()
serializer.serialize(output)

file = open('output.csv', 'wb')
file.write(output.getvalue())
file.close()

