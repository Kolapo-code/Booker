from flask import request, abort
from app import auth
from app.models.admin_user import AdminUser

def get_appointments():
	"""A function that gets all the appointments for the AdminUser."""
	session_id = auth.get_session_id(request)
	user_by_session = auth.get_user_by_session_id(request)
	if not user_by_session or not auth.check_session(session_id):
		abort(403, 'No session exists, or not allowed to access appointements')
	if not user_by_session.__class__ == "AdminUser":
		abort(403, 'Not allowed to access appointements')
	appointments = AdminUser.list_appointments()
	return appointments
