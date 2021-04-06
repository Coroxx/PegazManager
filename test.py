import json


# with open('test.json', 'r') as f:
#     data = json.load(f)
#     f.close


# print(data)
# num = 1

# l = []

# for element in list(data.items()):
#     del data[f'{element[0]}']
#     data[num] = {
#         "type": "key",
#         "ip": element[1]['ip'],
#         "port": element[1]['port'],
#         "username": element[1]['username'],
#         "path": element[1]['path'],

#     }
#     num += 1

#     with open('test.json', 'w') as f:
#         f.write(json.dumps(data,
#                            indent=4, separators=(',', ': ')))

num = 1
with open('test.json', 'r') as f:
    data = json.load(f)
    f.close()


for element in list(data.items()):
    del data[f'{element[0]}']
    data[num] = {
        "type": "key",
        "ip": element[1]['ip'],
        "port": element[1]['port'],
        "username": element[1]['username'],
        "path": element[1]['path'],

    }
    num += 1

    with open('test.json', 'w') as f:
        f.write(json.dumps(data,
                           indent=4, separators=(',', ': ')))
