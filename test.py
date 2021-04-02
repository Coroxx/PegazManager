import json


with open("config.json", 'r') as f:
    data = json.loads(f.read())  # data becomes a dictionary


for i in range(4):
    # do things with data here
    data[i] = {
        "ip": "12.3.4.2",
        "username": "root"
    }

# and then just write the data back on the file
with open("config.json", 'w') as f:
    f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
