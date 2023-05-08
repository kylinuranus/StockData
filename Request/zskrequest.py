
from enum import Enum
import requests
import json
import re

class requestMethod(Enum):
    POST = 1
    GET = 2
    

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
    except:
        raise ValueError('Invalid Input')
    
def request(method,url,params=None):
    
    
    if method == requestMethod.GET:
        r = requests.get(url,params=params)
        json1 = loads_jsonp(r.text)
        json_str = json.dumps(json1)
        data = json.loads(json_str)
        return data
    
    
        