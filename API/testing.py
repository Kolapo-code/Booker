from app import storage
from app.models.user import User

# user = User(name='Omar')
# storage.new(user)
# user = User(name='Abderrahim')
# storage.new(user)
# user = User(name='Abdellatif')
# storage.new(user)
# user = User(name='Abdelhak')
# storage.new(user)
# user = User(name='Ahmed')
# storage.new(user)
# user = User(name='Mariam', age='18')
# storage.new(user)
# storage.save()
# user = User(name='Mariam', age='30')
# storage.new(user)
# storage.save()

# data = storage.get('User', name='Mariam')

# for key, val in data.items():
#     storage.delete(val)
#     storage.save()

data = storage.get('User', name='Mariam', age=30)

# print(data)
for key, val in data.items():
    print(f'{key}: {val.to_dict()}')
