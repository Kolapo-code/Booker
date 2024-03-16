"""
This file stores configuration variables
for the Flask application.
"""
class DB_config:
    user = 'admin'
    passworld = 'admin'
    host = 'localhost'
    data_base = 'booker'
    url = f'mysql+mysqldb://{user}:{passworld}@{host}/{data_base}'
