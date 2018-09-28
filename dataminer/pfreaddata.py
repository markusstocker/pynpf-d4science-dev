# -*- coding: utf-8 -*-
import requests
import csv
from rdflib import Graph

globalvariables = None

with open('globalvariables.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    globalvariables = {rows[0]: rows[1] for rows in reader}

headers = {'Content-Type':'application/json',
           'Accept':'application/json',
           'gcube-token':globalvariables['gcube_token']}

g = Graph()

res = requests.get('http://catalogue-ws.d4science.org/catalogue-ws/rest/api/items/show',
                   params={'id':'npfe_descriptions_at_hyytiaelae'},
                   headers=headers)
json = res.json()

for resource in json['result']['resources']:
    g.parse(data=requests.get(resource['url']).content.decode('utf-8'), format="turtle")

res = requests.get('http://catalogue-ws.d4science.org/catalogue-ws/rest/api/items/show',
                   params={'id':'npfe_mean_durations'},
                   headers=headers)
json = res.json()

for resource in json['result']['resources']:
    g.parse(data=requests.get(resource['url']).content.decode('utf-8'), format="turtle")

g.serialize('output.ttl', format='turtle')

