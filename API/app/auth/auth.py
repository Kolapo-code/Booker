import base64
from app.engine.storage import DBStorage
from app.config import classes, EXPIRY
from app import storage
from app.models.session import Session


class Auth:
    """A class where we handle users authentication."""

    def get_session_id(self, request):
        """get session id from cookies"""
        return request.cookies.get('session_id')

    def check_session(self, session_id):
        """check """
        session = self.get_session(session_id)
        if session is None:
            return False
        if not session.check_expiry():
            self.delete_session(session)
            return False
        return True

    def get_session(self, session_id):
        if  session_id is None or session_id == '':
            return None
        sessions = storage.get('Session', id=session_id)
        if sessions == {}:
            return None
        session = list(sessions.values())[0]
        return session

    def get_user_by_session_id(self, request):
        session_id = self.get_session_id(self, request)
        session = self.get_session(session_id)
        if session is None:
            return None
        if not session.check_expiry():
            self.delete_session(session)
            return None
        return session.user

    def create_session(self, user_id):
        """return session id"""
        users = storage.get('RegularUser', id=user_id)
        if users == {}:
            return None
        user = list(users.values())[0]
        session = Session(expiry_time=EXPIRY, user_id=user.id)
        session.save()
        return session.id

    def delete_session(self, session):
        """delete session in database"""
        if session is None:
            return None
        storage.delete(session)
        storage.save()

    def check_email(self, email):
        """A method that checks if an email already registered in the database."""
        users = storage.get('RegularUser', email=email)
        if users == {}:
            return None
        return list(users.values())[0]

    def get_user_by_token(self, token):
        """A method that gets the user by the given token."""
        users = storage.get('RegularUser', token=token)
        if users == {}:
            return None
        return users
