# -*- coding: utf-8 -*-
import sys
import requests
import csv
from PIL import Image
from StringIO import StringIO
from dateutil import tz
from hashlib import md5
from pytz import timezone
from datetime import datetime
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

configuration = {
    'Hyytiaelae': {
        'identifier': URIRef('http://sws.geonames.org/656888/'),
        'name': 'Hyytiälä',
        'encoded_name':'hyytiaelae',
        'countryCode': 'FI',
        'locationMap': URIRef('http://www.geonames.org/656888/hyytiaelae.html'),
        'latitude': '61.84562',
        'longitude': '24.29077',
        'package_id_descriptions': 'npfe_descriptions_at_hyytiaelae',
        'package_id_plots': 'npfe_plots_at_hyytiaelae'
    },
    'Puijo': {
        'identifier': URIRef('http://sws.geonames.org/640784/'),
        'name': 'Puijo',
        'encoded_name': 'puijo',
        'countryCode': 'FI',
        'locationMap': URIRef('http://www.geonames.org/640784/puijo.html'),
        'latitude': '62.91667',
        'longitude': '27.65'
    },
    'Vaerrioe': {
        'identifier': URIRef('http://sws.geonames.org/828747/'),
        'name': 'Värriö',
        'encoded_name': 'vaerrioe',
        'countryCode': 'FI',
        'locationMap': URIRef('http://www.geonames.org/828747/vaerrioe.html'),
        'latitude': '67.46535',
        'longitude': '27.99231'
    },
    'Class Ia': {
        'identifier': URIRef('http://avaa.tdata.fi/web/smart/smear/ClassIa'),
        'label': 'Class Ia',
        'comment': 'Very clear and strong event'
    },
    'Class Ib': {
        'identifier': URIRef('http://avaa.tdata.fi/web/smart/smear/ClassIb'),
        'label': 'Class Ib',
        'comment': 'Unclear event'
    },
    'Class II': {
        'identifier': URIRef('http://avaa.tdata.fi/web/smart/smear/ClassII'),
        'label': 'Class II',
        'comment': 'Event with little confidence level'
    }
}

day = sys.argv[1]
place = sys.argv[2]
beginning = sys.argv[3]
end = sys.argv[4]
classification = sys.argv[5]
image = sys.argv[6]

#day = '2018-04-04'
#place = 'Hyytiaelae'
#beginning = '12:00'
#end = '13:30'
#classification = 'Class Ia'
#image = 'http://data.d4science.org/SE1HYU1EdzNkbU1LUFBnWHQ2M2NPb0h6Y2lidlVmNTBHbWJQNStIS0N6Yz0-VLT'

globalvariables = None

with open('globalvariables.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    globalvariables = {rows[0]: rows[1] for rows in reader}

point = 'POINT ({} {})'.format(configuration[place]['longitude'], configuration[place]['latitude'])

ns = 'http://avaa.tdata.fi/web/smart/smear/'
tz_helsinki = timezone('Europe/Helsinki')
beginning_datetime = tz_helsinki.localize(datetime.strptime('{} {}'.format(day, beginning), '%Y-%m-%d %H:%M'))
end_datetime = tz_helsinki.localize(datetime.strptime('{} {}'.format(day, end), '%Y-%m-%d %H:%M'))
beginning_isoformat = beginning_datetime.isoformat()
end_isoformat = end_datetime.isoformat()
time_isoformat = '{}/{}'.format(beginning_isoformat, end_isoformat)
datetime_now = datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

event_uri = URIRef('{}{}'.format(ns, md5('{}{}'.format(day, place).encode()).hexdigest()))
geometry_uri = URIRef('{}{}'.format(ns, md5(point.encode()).hexdigest()))
time_uri = URIRef('{}{}'.format(ns, md5(time_isoformat.encode()).hexdigest()))
beginning_uri = URIRef('{}{}'.format(ns, md5(beginning_isoformat.encode()).hexdigest()))
end_uri = URIRef('{}{}'.format(ns, md5(end_isoformat.encode()).hexdigest()))
place_uri = configuration[place]['identifier']
classification_uri = configuration[classification]['identifier']
image_uri = URIRef(image)
data_visualization_uri = URIRef('{}{}'.format(ns, md5('{}{}'.format(datetime_now, 'data_visualization').encode()).hexdigest()))

LODE = dict()
DUL = dict()
GeoNames = dict()
WGS84 = dict()
SMEAR = dict()
SimpleFeatures = dict()
GeoSPARQL = dict()
Time = dict()
PROV = dict()
OBO = dict()

LODE['Event'] = URIRef('http://linkedevents.org/ontology/Event')
LODE['atPlace'] = URIRef('http://linkedevents.org/ontology/atPlace')
LODE['atTime'] = URIRef('http://linkedevents.org/ontology/atTime')
LODE['inSpace'] = URIRef('http://linkedevents.org/ontology/inSpace')
LODE['involved'] = URIRef('http://linkedevents.org/ontology/involved')
DUL['Place'] = URIRef('http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#Place')
GeoNames['Feature'] = URIRef('http://www.geonames.org/ontology#Feature')
GeoNames['name'] = URIRef('http://www.geonames.org/ontology#name')
GeoNames['countryCode'] = URIRef('http://www.geonames.org/ontology#countryCode')
GeoNames['locationMap'] = URIRef('http://www.geonames.org/ontology#locationMap')
WGS84['SpatialThing'] = URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing')
WGS84['lat'] = URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#lat')
WGS84['long'] = URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#long')
SMEAR['Classification'] = URIRef('http://avaa.tdata.fi/web/smart/smear/Classification')
SMEAR['hasClassification'] = URIRef('http://avaa.tdata.fi/web/smart/smear/hasClassification')
SimpleFeatures['Point'] = URIRef('http://www.opengis.net/ont/sf#Point')
GeoSPARQL['asWKT'] = URIRef('http://www.opengis.net/ont/geosparql#asWKT')
GeoSPARQL['wktLiteral'] = URIRef('http://www.opengis.net/ont/geosparql#wktLiteral')
Time['Instant'] = URIRef('http://www.w3.org/2006/time#Instant')
Time['Interval'] = URIRef('http://www.w3.org/2006/time#Interval')
Time['TemporalUnit'] = URIRef('http://www.w3.org/2006/time#TemporalUnit')
Time['hasTime'] = URIRef('http://www.w3.org/2006/time#hasTime')
Time['hasBeginning'] = URIRef('http://www.w3.org/2006/time#hasBeginning')
Time['hasEnd'] = URIRef('http://www.w3.org/2006/time#hasEnd')
Time['inXSDDateTime'] = URIRef('http://www.w3.org/2006/time#inXSDDateTime')
PROV['Entity'] = URIRef('http://www.w3.org/ns/prov#Entity')
PROV['Activity'] = URIRef('http://www.w3.org/ns/prov#Activity')
PROV['Agent'] = URIRef('http://www.w3.org/ns/prov#Agent')
PROV['wasDerivedFrom'] = URIRef('http://www.w3.org/ns/prov#wasDerivedFrom')
PROV['wasGeneratedBy'] = URIRef('http://www.w3.org/ns/prov#wasGeneratedBy')
PROV['used'] = URIRef('http://www.w3.org/ns/prov#used')
PROV['startedAtTime'] = URIRef('http://www.w3.org/ns/prov#startedAtTime')
PROV['endedAtTime'] = URIRef('http://www.w3.org/ns/prov#endedAtTime')
OBO['data visualization'] = URIRef('http://purl.obolibrary.org/obo/OBI_0200111')

g = Graph()

g.bind('lode', 'http://linkedevents.org/ontology/')
g.bind('dul', 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#')
g.bind('gn', 'http://www.geonames.org/ontology#')
g.bind('wgs84', 'http://www.w3.org/2003/01/geo/wgs84_pos#')
g.bind('smear', 'http://avaa.tdata.fi/web/smart/smear/')
g.bind('sf', 'http://www.opengis.net/ont/sf#')
g.bind('geosparql', 'http://www.opengis.net/ont/geosparql#')
g.bind('time', 'http://www.w3.org/2006/time#')
g.bind('prov', 'http://www.w3.org/ns/prov#')

g.add((OBO['data visualization'], RDFS.label, Literal('data visualization')))

g.add((event_uri, RDF.type, LODE['Event']))
g.add((event_uri, LODE['atPlace'], place_uri))
g.add((event_uri, LODE['inSpace'], geometry_uri))
g.add((event_uri, LODE['atTime'], time_uri))
g.add((event_uri, SMEAR['hasClassification'], classification_uri))
g.add((place_uri, RDF.type, DUL['Place']))
g.add((place_uri, RDF.type, GeoNames['Feature']))
g.add((place_uri, GeoNames['name'], Literal(configuration[place]['name'], datatype=XSD.string)))
g.add((place_uri, GeoNames['countryCode'], Literal(configuration[place]['countryCode'], datatype=XSD.string)))
g.add((place_uri, GeoNames['locationMap'], configuration[place]['locationMap']))
g.add((place_uri, WGS84['lat'], Literal(configuration[place]['latitude'], datatype=XSD.double)))
g.add((place_uri, WGS84['long'], Literal(configuration[place]['longitude'], datatype=XSD.double)))
g.add((classification_uri, RDF.type, SMEAR['Classification']))
g.add((classification_uri, RDFS.label, Literal(configuration[classification]['label'], datatype=XSD.string)))
g.add((classification_uri, RDFS.comment, Literal(configuration[classification]['comment'], datatype=XSD.string)))
g.add((geometry_uri, RDF.type, SimpleFeatures['Point']))
g.add((geometry_uri, RDF.type, WGS84['SpatialThing']))
g.add((geometry_uri, GeoSPARQL['asWKT'], Literal(point, datatype=GeoSPARQL['wktLiteral'])))
g.add((time_uri, RDF.type, Time['Interval']))
g.add((time_uri, Time['hasBeginning'], beginning_uri))
g.add((time_uri, Time['hasEnd'], end_uri))
g.add((beginning_uri, RDF.type, Time['Instant']))
g.add((beginning_uri, Time['inXSDDateTime'], Literal(beginning_isoformat, datatype=XSD.dateTime)))
g.add((end_uri, RDF.type, Time['Instant']))
g.add((end_uri, Time['inXSDDateTime'], Literal(end_isoformat, datatype=XSD.dateTime)))

g.add((image_uri, RDF.type, PROV['Entity']))
g.add((event_uri, RDF.type, PROV['Entity']))
g.add((data_visualization_uri, RDF.type, PROV['Activity']))
g.add((data_visualization_uri, RDF.type, OBO['data visualization']))
g.add((event_uri, PROV['wasDerivedFrom'], image_uri))
g.add((event_uri, PROV['wasGeneratedBy'], data_visualization_uri))
g.add((data_visualization_uri, PROV['used'], image_uri))
g.add((data_visualization_uri, PROV['startedAtTime'], Literal(datetime_now.isoformat(), datatype=XSD.dateTime)))
g.add((data_visualization_uri, PROV['endedAtTime'], Literal(datetime_now.isoformat(), datatype=XSD.dateTime)))

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
                    params={'name':'{}-{}-description.ttl'.format(configuration[place]['encoded_name'], day),
                            'description':'New particle formation event description for {} on {}'.format(place, day),
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
                    json={'package_id':configuration[place]['package_id_descriptions'],
                          'name':'{}-{}-description'.format(configuration[place]['encoded_name'], day),
                          'url':path,
                          'format':'Turtle',
                          'mimetype':'application/x-turtle'},
                    headers=headers)

res = requests.get(image)
img = StringIO(res.content)

res = requests.post('https://workspace-repository.d4science.org/home-library-webapp/rest/Upload',
                    params={'name':'{}-{}-plot.png'.format(configuration[place]['encoded_name'], day),
                            'description':'New particle formation event plot for {} on {}'.format(place, day),
                            'parentPath':'/Home/{}/Workspace/{}'.format(globalvariables['gcube_username'], folder),
                            'mimetype':'image/png'},
                    data=img,
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

res = requests.post('http://catalogue-ws.d4science.org/catalogue-ws/rest/api/resources/create/',
                    json={'package_id':configuration[place]['package_id_plots'],
                          'name':'{}-{}-plot'.format(configuration[place]['encoded_name'], day),
                          'url':path,
                          'format':'PNG',
                          'mimetype':'image/png'},
                    headers=headers)