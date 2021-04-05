import json


with open('test.json', 'r') as f:
    info = json.load(f)
    f.close()

print(info)

num = 1

print(info)
for element in info:
    dd = list(element[1])
    num += 1


print(dd)

# with open('test.json', 'w') as f:
#     json.dump(info, f, indent=4)
