import json


with open("config.json", 'a') as f:
    data = """ 
        {"type": "pd"
        } """
    data = json.loads(data)
    json.dump(data, f, indent=2)
    f.write(',')
    f.close()
