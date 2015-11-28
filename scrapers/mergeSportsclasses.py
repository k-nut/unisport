import json
import os

JSON_PATH = os.environ.get('UNISPORT_JSON_PATH')

with open(os.path.join(JSON_PATH, 'hu.json')) as infile:
    hu = json.loads(infile.read())
with open(os.path.join(JSON_PATH, 'fu.json')) as infile:
    fu = json.loads(infile.read()) 
with open(os.path.join(JSON_PATH, 'htw.json')) as infile:
    htw = json.loads(infile.read())
with open(os.path.join(JSON_PATH, 'beuth.json')) as infile:
    beuth = json.loads(infile.read())        
with open(os.path.join(JSON_PATH, 'tu.json')) as infile:
    tu = json.loads(infile.read())      

with open(os.path.join(JSON_PATH, 'alle.json'), 'w') as outfile:
    outfile.write(json.dumps(hu[1:] + fu[1:] + beuth[1:] + htw[1:] + tu))

