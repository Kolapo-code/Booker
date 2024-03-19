from flask import Flask, jsonify
from app.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "notfound"}), 404


if __name__ == "__main__":
    """app runner"""
    app.run(host='0.0.0.0', port='5000', threaded=True)
