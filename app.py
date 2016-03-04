"""
This is a simple cheatsheet webapp.
"""
import os

from flask import Flask, send_from_directory

DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(DIR, 'docs', '_build', 'html')

app = Flask(__name__)

@app.route('/<path:path>')
def static_proxy(path):
    """Static files proxy"""
    return send_from_directory(ROOT, path)

@app.route('/')
def index_redirection():
    """Redirecting index file"""
    return send_from_directory(ROOT, 'index.html')

@app.route('/.well-known/acme-challenge/ojASzRypK5pQC2tedqCle9ezlVMF0BhfEwb4n1-L_k0')
def letsencrypt():
    return "ojASzRypK5pQC2tedqCle9ezlVMF0BhfEwb4n1-L_k0.fqEt_5js_qhcwlQwcUBLIIAMmE_Hh7ipfKTeYWyMBvs" 

if __name__ == "__main__":
    app.run(debug=True)
