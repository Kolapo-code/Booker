from app.engine.storage import DBStorage

storage = DBStorage()
storage.drop()
storage.reload()


from app.auth.auth import Auth

auth = Auth()
