from flask import Flask, jsonify
from app.views import app_views
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)



@app.errorhandler(400)
def bad_request(error) -> str:
    """Unauthorized handler"""
    if error.description:
        return jsonify({"error": error.description}), 400
    return jsonify({"error": "Bad Request"}), 400


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    if error.description:
        return jsonify({"error": error.description}), 401
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    if error.description:
        return jsonify({"error": error.description}), 403
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """Forbidden handler"""
    if error.description:
        return jsonify({"error": error.description}), 404
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    """app runner"""
    app.run(host="0.0.0.0", port="5000", threaded=True)
