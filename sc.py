from pycricbuzz import Cricbuzz
import json 
c = Cricbuzz()
matches=c.matches()
print (json.dumps(matches,indent=4)) #for pretty prinitng
