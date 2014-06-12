import flask
from flask import Flask
from flask import request

from provider import ShiftAuthorizationProvider

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


# OAuth2 Enabled Routes.
@app.route("/v1/oauth2/auth", methods=["GET"])
def authorization_code():
    provider = ShiftAuthorizationProvider()

    response = provider.get_authorization_code_from_uri(request.url)

    flask_res = flask.make_response(response.text, response.status_code)
    for k, v in response.headers.iteritems():
        flask_res.headers[k] = v
    return flask_res

@app.route("/v1/oauth2/token", methods=["POST"])
def token():
    provider = ShiftAuthorizationProvider()

    data = {k: request.form[k] for k in request.form.iterkeys()}  # dict comprehension?!

    response = provider.get_token_from_post_data(data)

    flask_res = flask.make_response(response.text, response.status_code)
    for k, v in response.headers.iteritems():
        flask_res.headers[k] = v
    return flask_res


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
