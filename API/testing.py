# fields = {
#     "title": (str, 60, 3),
#     "feild": (str, 60, 3),
#     "description": (str, 500, 150),
#     "picture": (str, 256, 0),
#     "schedules": (str, 256, 0),
#     "location": (str, 256, 30),
#     "contact": (str, 256, 5),
# }
# data = {
#     "feild": "devolopment",
#     "schedules": "00:00 to 06:00 AM",
#     "title": "Api Builder",
#     "picture": "",
#     "location": "Massa, Chtouka ait baha, Souss Massa",
#     "contact": "",
#     "description": "Drive consistency in naming Publish private and public schemas Share and learn from a centralized repository",
# }

# error = []
# list(map(lambda x: error.append(x[0])\
#     if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
#         not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
#         else x, data.items()))
# if error:
#     print(f'some field not set correctly : {", ".join(error)}')

# fields_keys = set(fields.keys())
# data_keys = set(data.keys())
# print(fields_keys)
# print(data_keys)
# error_str = ""
# if fields_keys != data_keys:
#     print("hello")
#     if fields_keys - data_keys:
#         error_str += f"{' '.join(fields_keys- data_keys)} missing"
#     if data_keys - fields_keys:
#         error_str += " and " if error_str else ""
#         error_str += f"{' '.join(data_keys- fields_keys)} do not exist"
#     print(error_str)
#     exit()
# print("all good")

import datetime

schedules = {
    "days": {
        "manday": {"from": "08:00", "to": "18:00"},
        "tuesday": {"from": "08:00", "to": "18:00"},
        "wednesday": {"from": "08:00", "to": "18:00"},
        "thursday": {"from": "08:00", "to": "18:00"},
        "friday": {
            "from": "08:00",
            "break": {"from": "12:00", "to": "14:00"},
            "to": "18:00",
        },
        "saturday": {"from": "08:00", "to": "12:00"},
        "sunday": {"from": "00:00", "to": "00:00"},
    }
}

schedule_dict = {
    "days": {
        "manday": {},
        "tuesday": {},
        "wednesday": {},
        "thursday": {},
        "friday": {},
        "saturday": {},
        "sunday": {}
    }
}
if set(schedule_dict.keys()) != {'days'}:
    print("Make sure you set up the key [days].")
days_set = set(schedule_dict["days"].keys())
data_set = set(schedules['days'].keys())
error_string = ""
if days_set != data_set:
    extra = days_set - data_set
    missing = data_set - days_set
    if missing:
        error_string += f"Make sure you add {', '.join(missing)} to the days"
    error_string += " and " if error_string else ""
    if extra:
        error_string += f"remove {', '.join(extra)} from the days"
print(error_string)

for day in schedules["days"].keys():
    print(schedules['days'][day].keys() )
    if set(schedules['days'][day].keys()) not in ["from", "to", "break"]:
        print("The data keys in each day should be one of the following: [from], [to], [break]")
    try:
        if schedules['days'][day]["from"]:
            schedule_dict['days'][day]["from"] = datetime.strptime(schedules['days'][day]["from"])
        if schedules['days'][day]["to"]:
            schedule_dict['days'][day]["to"] = datetime.strptime(schedules['days'][day]["to"])
        if schedules['days'][day]["break"]:
            schedule_dict['days'][day]["break"] = datetime.strptime(schedules['days'][day]["break"])
    except(ValueError,TypeError):
        print("the keys were set incorrectly, follow the format : %H:%M.")
print(schedule_dict)
