"""
This is a simple cheatsheet webapp.
"""
import os

from flask import Flask, send_from_directory
from flask_sslify import SSLify

DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(DIR, 'docs', '_build', 'html')

app = Flask(__name__)
#if 'DYNO' in os.environ:
#        sslify = SSLify(app)

@app.route('/<path:path>')
def static_proxy(path):
    """Static files proxy"""
    return send_from_directory(ROOT, path)

@app.route('/')
def index_redirection():
    """Redirecting index file"""
    return send_from_directory(ROOT, 'index.html')

@app.route('/.well-known/acme-challenge/39LkboWlzrvSn4bGSC-vx5Ea4FqKipU5QYcLKAn1hSM')
def letsencrypt():
    return "39LkboWlzrvSn4bGSC-vx5Ea4FqKipU5QYcLKAn1hSM.1MQ2tN97oDMCS6VnIiDMXAjUQwpiEoyNT2mUiGLhR7o"

if __name__ == "__main__":
    app.run(debug=True)
