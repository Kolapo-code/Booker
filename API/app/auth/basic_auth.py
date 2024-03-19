import base64
from app.engine.storage import DBStorage
from app.config import classes


class BasicAuth:
    """A class where we handle users authentication."""

    def extract_header(self, request=None):
        """A method that extracts the authorization header from a request."""
        return (
            None
            if not request or "Authorization" not in request.headers
            else request.headers["Authorization"]
        )

    def extract_base64_header(self, authorization_header):
        """A method that extracts the base64 from the authorization header."""
        if (
            authorization_header is not None
            and isinstance(authorization_header, str)
            and authorization_header.startswith("Basic ")
        ):
            return authorization_header[6:]
        return None

    def decode_base64_header(self, base64_authorization_header):
        """A method that decodes the base 64 authorization header."""
        if base64_authorization_header is not None and isinstance(
            base64_authorization_header, str
        ):
            try:
                decoded_bytes = base64.b64decode(base64_authorization_header)
                return decoded_bytes.decode("utf-8")
            except (base64.binascci.Error, UnicodeError):
                return None
        return None

    def extract_credentials(self, decoded_base64_authorization_header):
        """A method that extract the credentials from the decoded base 64 header."""
        if (
            decoded_base64_authorization_header is not None
            and isinstance(decoded_base64_authorization_header, str)
            and ":" in decoded_base64_authorization_header
        ):
            user, password = decoded_base64_authorization_header.split(":", 1)
            return (user, password)
        return None

    def get_by_credentials(self, email, password):
        """A method that gets the object by the credentials."""
        if email and isinstance(email, str) and password and isinstance(password, str):
            regular_users = DBStorage.get(
                classes["RegularUser"], {"email": email, "password": password}
            )
            if regular_users:
                for regular_user in regular_users:
                    if regular_user.check_password(password):
                        return regular_user
            premium_users = DBStorage.get(
                classes["PremiumUser"], {"email": email, "password": password}
            )
            if premium_users:
                for premium_user in premium_users:
                    if premium_user.check_password(password):
                        return premium_user
            return None
        return None

    def current_user(self, request=None):
        """A method that retreives the user instance by following the basicAuth's steps."""
        header = self.extract_header(request)
        header_base64 = self.extract_base64_header(header)
        header_decode = self.decode_base64_header(header_base64)
        user_email, user_password = self.extract_credentials(header_decode)
        user = self.get_by_credentials(user_email, user_password)
        return user
