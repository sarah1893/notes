import unittest
import requests
import os

from flask_testing import LiveServerTestCase

from app import find_key
from app import ROOT
from app import app


class PysheeetTest(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_redirection(self):
        url = self.get_server_url()
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_static_proxy(self):
        htmls = os.listdir(os.path.join(ROOT, 'notes'))
        url = self.get_server_url()
        for h in htmls:
            u = url + '/notes/' + h
            resp = requests.get(u)
            self.assertEqual(resp.status_code, 200)

    def test_find_key(self):
        token = 'token'
        key = "key"
        os.environ['ACME_TOKEN'] = token
        os.environ['ACME_KEY'] = key
        self.assertEqual(find_key(token), key)

        del os.environ['ACME_TOKEN']
        del os.environ['ACME_KEY']

        os.environ['ACME_TOKEN_ENV'] = token
        os.environ['ACME_KEY_ENV'] = key
        self.assertEqual(find_key(token), key)

        del os.environ['ACME_TOKEN_ENV']
        del os.environ['ACME_KEY_ENV']

    def test_acme(self):
        # remove env ACME_TOKEN*
        for k, v in os.environ.items():
            if not k.startswith("ACME_TOKEN"):
                continue
            del os.environ[k]

        url = self.get_server_url()
        u = url + '/.well-known/acme-challenge/token'
        resp = requests.get(u)
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
