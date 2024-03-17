from app import storage
from app.models.user import User, BaseModel

# user = User(name='Omar')
# storage.new(user)
# user = User(name='Abderrahim')
# storage.new(user)
# user = User(name='Abdellatif', age='14')
# user.save()
# user = User(name='Abdelhak', age='20')
# user.save()
# user = User(name='Ahmed', age='27')
# user.save()
# user = User(name='Mariam', age='18')
# user.save()
# storage.save()
# user = User(name='Mariam', age='30')
# user.save()


# data = storage.get('User', name='Mariam')

# for key, val in data.items():
#     storage.delete(val)
#     storage.save()

data = storage.get('User')

# print(data)
for key, val in data.items():
    print(f'{key}: {val.to_dict()}')

print(BaseModel.activity_log())
