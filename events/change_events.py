import json

from tomlkit import value

event = '../events/full_test_event.json'
with open(event, 'r') as file:
    data = json.load(file)


for key, value in data.items():
    # print(value)
    for item in value:
        item['email'] = 'cast.ses.1@efs.at'

print(data)

event2 = '../events/full_test_event.json'



with open(event2, 'w') as file:
    json.dump(data, file)

    # with open("../test_data/sendinglist.json", "w") as outfile:
    #     json.dump(sending_list, outfile)
