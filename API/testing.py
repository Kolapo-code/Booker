from app import storage
# import base64
# from Booker.API.app.models.user import User, RegularUser
# from app.models.premium_user import PremiumUser
from datetime import datetime

# user = RegularUser(
#     first_name="Asmaa",
#     last_name="Hadar",
#     email="asmaehadar32@gmail.com",
#     password=base64.b64encode(b"helloo"),
#     birth_date=datetime(1980, 11, 4),
#     location="Morocco",
# )
# storage.new(user)
# print(user.check_password(base64.b64encode(b"helloo")))
# storage.save()
# storage.get("RegularUser")
# user = RegularUser(
#     first_name="Omar",
#     last_name="Idhmaid",
#     email="omaridhmaid@gmail.com",
#     password=base64.b64encode("hellooo".encode("utf-8")),
#     birth_date=datetime(1927, 2, 28),
#     location="Colombia",
# )
# user.save()
# storage.new(user)
# print(user.check_password(base64.b64encode("hellooo".encode("utf-8"))))
# storage.delete()

# print(user.check_password(base64.b64encode("hellooo".encode("utf-8"))))

# user = PremiumUser(
#     first_name="Asmaa",
#     last_name="Hadar",
#     email="asmaehadar32@gmail.com",
#     password="hi",
#     birth_date=datetime(1980, 11, 4),
#     location="Morocco",
#     field="IT",
#     biography="EMMMM",
#     subscription_start_date=datetime.now(),
#     subscription_end_date=datetime.now(),
#     subscription_plan="something",
#     subscription_status="Pending",
# )
# storage.new(user)
# print(user.check_password("hi"))

# user = User(name="Abderrahim")
# storage.new(user)
# user = User(name="Abdellatif", age="14")
# user.save()
# user = User(name="Abdelhak", age="20")
# user.save()
# user = User(name="Ahmed", age="27")
# user.save()
# user = User(name="Mariam", age="18")
# user.save()
# storage.save()
# user = RegularUser(
#     first_name="Mariam",
#     last_name="Makaynach",
#     email="RahMakaynach@booker.net",
#     password="a%dz5223-rea43f9faf",
# )
# user.save()


# data = storage.get()

# for key, val in data.items():
#     storage.delete(val)
#     storage.save()

data = storage.get("RegularUser")

# # print(data)
for key, val in data.items():
    print(f"{key}: {val.to_dict()}")

# car_dict = {
#     "a": "Mercedes-Benz",
#     "b": "BMW",
#     "c": "Ferrari",
#     "d": "Lamborghini",
#     "e": "Jeep",
# }


# car_dict = dict(filter(lambda x: x[0] != "a", car_dict.items()))
