import json
import sqlalchemy

with open('/home/knut/sportsClasses/hu.json') as infile:
    hu = json.loads(infile.read())
with open('/home/knut/sportsClasses/fu.json') as infile:
    fu = json.loads(infile.read()) 
with open('/home/knut/sportsClasses/htw.json') as infile:
    htw = json.loads(infile.read())
with open('/home/knut/sportsClasses/beuth.json') as infile:
    beuth = json.loads(infile.read())        
with open('/home/knut/sportsClasses/tu.json') as infile:
    tu = json.loads(infile.read())      

with open('/home/knut/unisport/alle.json', 'w') as outfile:
    outfile.write(json.dumps(hu[1:] + fu[1:] + beuth[1:] + htw[1:] + tu))

