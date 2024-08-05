
m flask import abort, Blueprint

app_views = Blueprint('app_views', __name__)

@app_views.route('/api/v1/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized():
        """Endpoint to raise a 401 error."""
            abort(401)

@app_views.route('/api/v1/forbidden', methods=['GET'], strict_slashes=False)
def forbidden():
        """Endpoint to raise a 403 error."""
            abort(403)
