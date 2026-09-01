"""Sample Flask application for the GitHub Actions demo."""

import os
import platform
import socket

from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.environ.get("APP_NAME", "Aviz Academy GHA Demo")


@app.route("/")
def home():
    return f"""<html>
    <head><title>{APP_NAME}</title></head>
    <body>
        <h1>Hello, This deployment is from GithubActions</h1>
        <h2>Served by gunicorn as a non-root user</h2>
        <p>Container host: {socket.gethostname()}</p>
        <p>Running as UID: {os.getuid()}</p>
        <p>Python: {platform.python_version()}</p>
    </body>
</html>"""


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/api/info")
def info():
    return jsonify(
        app=APP_NAME,
        hostname=socket.gethostname(),
        uid=os.getuid(),
        python=platform.python_version(),
    )


if __name__ == "__main__":
    # Local development only; the container runs gunicorn instead.
    # Debugger stays off unless FLASK_DEBUG=1 is set explicitly.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=8000, debug=debug)
