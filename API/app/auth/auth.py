from app.config import EXPIRY
from app import storage
from app.models.session import Session


class Auth:
    """A class where we handle users authentication."""

    def get_session_id(self, request):
        """get session id from cookies"""
        return request.cookies.get("session_id")

    def check_session(self, session_id):
        """A method that checks the existance of a session"""
        session = self.get_session(session_id)
        if session is None:
            return False
        if not session.check_expiry():
            self.delete_session(session)
            return False
        return True

    def get_session(self, session_id):
        """A method that gets a session from db."""
        if session_id is None or session_id == "":
            return None
        sessions = storage.get("Session", id=session_id)
        if sessions == {}:
            return None
        session = list(sessions.values())[0]
        return session

    def get_user_by_session_id(self, request):
        """A method that gets a user by the session id."""
        session_id = self.get_session_id(request)
        session = self.get_session(session_id)
        if session is None:
            return None
        if not session.check_expiry():
            self.delete_session(session)
            return None
        return session.user

    def create_session(self, user_id):
        """A method that creates a new session using the user_id."""
        users = storage.get("User", id=user_id)
        if users == {}:
            return None
        user = list(users.values())[0]
        session = Session(expiry_time=EXPIRY, user_id=user.id)
        session.save()
        return session.id

    def delete_session(self, session):
        """A method that deletes a session from db."""
        if session is None:
            return None
        storage.delete(session)
        storage.save()

    def check_email(self, email):
        """A method that checks if an email already registered in the database."""
        users = storage.get("User", email=email)
        if users == {}:
            return None
        return list(users.values())[0]

    def get_user_by_token(self, token):
        """A method that gets the user by the given token."""
        users = storage.get("User", token=token)
        if users == {}:
            return None
        return users
