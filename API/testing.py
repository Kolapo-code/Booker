fields = {
    "title": (str, 60, 3),
    "feild": (str, 60, 3),
    "description": (str, 500, 150),
    "picture": (str, 256, 0),
    "schedules": (str, 256, 0),
    "location": (str, 256, 30),
    "contact": (str, 256, 5),
}
data = {
    "feild": "devolopment",
    "schedules": "00:00 to 06:00 AM",
    "title": "Api Builder",
    "picture": "",
    "location": "Massa, Chtouka ait baha, Souss Massa",
    "contact": "",
    "description": "Drive consistency in naming Publish private and public schemas Share and learn from a centralized repository",
}

# error = []
# list(map(lambda x: error.append(x[0])\
#     if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
#         not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
#         else x, data.items()))
# if error:
#     print(f'some field not set correctly : {", ".join(error)}')

fields_keys = set(fields.keys())
data_keys = set(data.keys())
print(fields_keys)
print(data_keys)
error_str = ""
if fields_keys != data_keys:
    print("hello")
    if fields_keys - data_keys:
        error_str += f"{' '.join(fields_keys- data_keys)} missing"
    if data_keys - fields_keys:
        error_str += " and " if error_str else ""
        error_str += f"{' '.join(data_keys- fields_keys)} do not exist"
    print(error_str)
    exit()
print("all good")
