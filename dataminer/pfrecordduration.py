# -*- coding: utf-8 -*-
import sys
import requests
import csv
from dateutil import tz
from hashlib import md5
from datetime import datetime
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

value = sys.argv[1]
event_uris = sys.argv[2]

#value = '1.6'
#event_uris = 'http://avaa.tdata.fi/web/smart/smear/2c3514176ca67a77a99292cbb4b6a3ae'

event_uris = event_uris.split(',')

unit = 'hour'
datetime_now = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

globalvariables = None

with open('globalvariables.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    globalvariables = {rows[0]: rows[1] for rows in reader}

ns = 'http://avaa.tdata.fi/web/smart/smear/'

obo = dict()
prov = dict()

obo['scalar measurement datum'] = URIRef('http://purl.obolibrary.org/obo/IAO_0000032')
obo['has measurement unit label'] = URIRef('http://purl.obolibrary.org/obo/IAO_0000039')
obo['has measurement value'] = URIRef('http://purl.obolibrary.org/obo/IAO_0000004')
obo['time unit'] = URIRef('http://purl.obolibrary.org/obo/UO_0000003')
obo['hour'] = URIRef('http://purl.obolibrary.org/obo/UO_0000032')
obo['average value'] = URIRef('http://purl.obolibrary.org/obo/OBI_0000679')
obo['is_specified_output_of'] = URIRef('http://purl.obolibrary.org/obo/OBI_0000312')
obo['has_specified_output'] = URIRef('http://purl.obolibrary.org/obo/OBI_0000299')
obo['arithmetic mean calculation'] = URIRef('http://purl.obolibrary.org/obo/OBI_0200079')
obo['has_specified_input'] = URIRef('http://purl.obolibrary.org/obo/OBI_0000293')
obo['data set'] = URIRef('http://purl.obolibrary.org/obo/IAO_0000100')
obo['has part'] = URIRef('http://purl.obolibrary.org/obo/BFO_0000051')
obo['data item'] = URIRef('http://purl.obolibrary.org/obo/IAO_0000027')

prov['Entity'] = URIRef('http://www.w3.org/ns/prov#Entity')
prov['Activity'] = URIRef('http://www.w3.org/ns/prov#Activity')
prov['Agent'] = URIRef('http://www.w3.org/ns/prov#Agent')
prov['wasDerivedFrom'] = URIRef('http://www.w3.org/ns/prov#wasDerivedFrom')
prov['wasGeneratedBy'] = URIRef('http://www.w3.org/ns/prov#wasGeneratedBy')
prov['used'] = URIRef('http://www.w3.org/ns/prov#used')
prov['startedAtTime'] = URIRef('http://www.w3.org/ns/prov#startedAtTime')
prov['endedAtTime'] = URIRef('http://www.w3.org/ns/prov#endedAtTime')

datum_uri = URIRef('{}{}'.format(ns, md5('{}{}'.format(value, unit).encode()).hexdigest()))
arithmetic_mean_calculation_uri = URIRef('{}{}'.format(ns, md5('{}{}'.format(datetime_now, 'arithmetic_mean_calculation').encode()).hexdigest()))
dataset_uri = URIRef('{}{}'.format(ns, md5('{}{}'.format(datetime_now, 'dataset').encode()).hexdigest()))

g = Graph()
g.bind('obo', 'http://purl.obolibrary.org/obo/')
g.bind('prov', 'http://www.w3.org/ns/prov#')

g.add((obo['scalar measurement datum'], RDFS.label, Literal('scalar measurement datum')))
g.add((obo['has measurement unit label'], RDFS.label, Literal('has measurement unit label')))
g.add((obo['has measurement value'], RDFS.label, Literal('has measurement value')))
g.add((obo['time unit'], RDFS.label, Literal('time unit')))
g.add((obo['hour'], RDFS.label, Literal('hour')))
g.add((obo['average value'], RDFS.label, Literal('average value')))
g.add((obo['is_specified_output_of'], RDFS.label, Literal('is_specified_output_of')))
g.add((obo['has_specified_output'], RDFS.label, Literal('has_specified_output')))
g.add((obo['arithmetic mean calculation'], RDFS.label, Literal('arithmetic mean calculation')))
g.add((obo['has_specified_input'], RDFS.label, Literal('has_specified_input')))
g.add((obo['data set'], RDFS.label, Literal('data set')))
g.add((obo['has part'], RDFS.label, Literal('has part')))
g.add((obo['data item'], RDFS.label, Literal('data item')))

g.add((obo['hour'], RDF.type, obo['time unit']))
g.add((arithmetic_mean_calculation_uri, RDF.type, obo['arithmetic mean calculation']))
g.add((dataset_uri, RDF.type, obo['data set']))
g.add((datum_uri, RDF.type, obo['scalar measurement datum']))
g.add((datum_uri, RDF.type, obo['average value']))

g.add((datum_uri, obo['has measurement value'], Literal(value, datatype=XSD.decimal)))
g.add((datum_uri, obo['has measurement unit label'], obo['hour']))
g.add((datum_uri, obo['is_specified_output_of'], arithmetic_mean_calculation_uri))
g.add((arithmetic_mean_calculation_uri, obo['has_specified_output'], datum_uri))
g.add((arithmetic_mean_calculation_uri, obo['has_specified_input'], dataset_uri))

for event_uri in event_uris:
    g.add((URIRef(event_uri), RDF.type, obo['data item']))
    g.add((dataset_uri, obo['has part'], URIRef(event_uri)))

g.add((dataset_uri, RDF.type, prov['Entity']))
g.add((datum_uri, RDF.type, prov['Entity']))
g.add((arithmetic_mean_calculation_uri, RDF.type, prov['Activity']))
g.add((datum_uri, prov['wasDerivedFrom'], dataset_uri))
g.add((datum_uri, prov['wasGeneratedBy'], arithmetic_mean_calculation_uri))
g.add((arithmetic_mean_calculation_uri, prov['used'], dataset_uri))
g.add((arithmetic_mean_calculation_uri, prov['startedAtTime'], Literal(datetime_now.isoformat(), datatype=XSD.dateTime)))
g.add((arithmetic_mean_calculation_uri, prov['endedAtTime'], Literal(datetime_now.isoformat(), datatype=XSD.dateTime)))

headers = {'Content-Type':'application/x-turtle',
           'Accept':'application/xml',
           'gcube-token':globalvariables['gcube_token']}

# First needs to check if the folder exists
folder = 'Data'

res = requests.get('https://workspace-repository.d4science.org/home-library-webapp/rest/List',
                   params={'absPath':'/Home/{}/{}'.format(globalvariables['gcube_username'], folder),
                           'secureUrl':'true'},
                   headers=headers)

if 'ItemNotFoundException' in res.text:
    res = requests.post('https://workspace-repository.d4science.org/home-library-webapp/rest/CreateFolder',
                        params={'name': folder,
                                'description': 'Data generated in NPFE classification and processing',
                                'parentPath': '/Home/{}/Workspace'.format(globalvariables['gcube_username'])},
                        headers=headers)


res = requests.post('https://workspace-repository.d4science.org/home-library-webapp/rest/Upload',
                    params={'name':'{}-npfe-mean-duration.ttl'.format(datetime_now.strftime('%Y-%m-%dT%H%M%S')),
                            'description':'Mean event duration computed on {}'.format(datetime_now.strftime('%Y-%m-%d %H:%M:%S')),
                            'parentPath':'/Home/{}/Workspace/{}'.format(globalvariables['gcube_username'], folder),
                            'mimetype':'application/x-turtle'},
                    data=g.serialize(format='turtle'),
                    headers=headers)

path = res.text

path = path.replace('<string>','')
path = path.replace('</string>','')

res = requests.get('https://workspace-repository.d4science.org/home-library-webapp/rest/GetPublicLink',
                   params={'absPath':'/Home/{}{}'.format(globalvariables['gcube_username'], path),
                           'secureUrl':'true'},
                   headers=headers)

path = res.text

path = path.replace('<string>','')
path = path.replace('</string>','')

headers = {'Content-Type':'application/json',
           'Accept':'application/json',
           'gcube-token':globalvariables['gcube_token']}

res = requests.post('http://catalogue-ws.d4science.org/catalogue-ws/rest/api/resources/create/',
                    json={'package_id':'npfe_mean_durations',
                          'name':'{}-npfe-mean-duration'.format(datetime_now.strftime('%Y-%m-%dT%H%M%S')),
                          'url':path,
                          'format':'Turtle',
                          'mimetype':'application/x-turtle'},
                    headers=headers)