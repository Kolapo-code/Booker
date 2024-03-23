requirements = {
        "title": (str, 60, 3),
        "feild": (str, 60, 3),
        "description": (str, 500, 150),
        "picture": (str, 256, 0),
        "schedules": (str, 256, 0),
        "location": (str, 256, 30),
        "contact": (str, 256, 5)
    }
data = {
        "feild": "devolopment",
        "schedules": "00:00 to 06:00 AM",
        "title": "Api Builder",
        "picture": "",
        "contact": "0639428008",
        "location": "Massa, Chtouka ait baha, Souss Massa",
        "description": "Drive consistency in naming Publish private and public schemas Share and learn from a centralized repository"
}

error = []
list(map(lambda x: error.append(x[0])\
    if x[0] not in requirements or not isinstance(x[1], requirements[x[0]][0]) or\
        not (requirements[x[0]][2] <= len(x[1]) < requirements[x[0]][1])\
        else x, data.items()))
if error:
    print(f'some field not set correctly : {", ".join(error)}')
