import requests

bindings = """
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix tmpl: <http://openprovenance.org/tmpl#> .
@prefix var: <http://openprovenance.org/var#> .

var:image a prov:Entity ;
  tmpl:value_0 <https://data.d4science.org/MzhkMUdQZmRrSkxOc2kzWHA0amdlNlZTbW5yRWdGdUZHbWJQNStIS0N6Yz0> .
"""

expand = 'https://envriplus-provenance.test.fedcloud.eu/templates/5bb24bfad6fa333a440a6613/expand'

res = requests.get(expand, params={'bindings': bindings})

print(res.url)
print(res.text)

