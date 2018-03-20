import unittest
import requests
import os

from werkzeug.exceptions import NotFound
from flask_testing import LiveServerTestCase

from app import (
    acme,
    find_key,
    static_proxy,
    index_redirection
)

from app import ROOT
from app import app


class PysheeetTest(LiveServerTestCase):

    def create_app(self):

        # remove env ACME_TOKEN*
        for k, v in os.environ.items():
            if not k.startswith("ACME_TOKEN"):
                continue
            del os.environ[k]

        self.token = 'token'
        self.key = "key"
        os.environ['ACME_TOKEN'] = self.token
        os.environ['ACME_KEY'] = self.key
        app.config['TESTING'] = True
        return app

    def test_index_redirection_req(self):
        url = self.get_server_url()
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_static_proxy_req(self):
        htmls = os.listdir(os.path.join(ROOT, 'notes'))
        url = self.get_server_url()
        for h in htmls:
            u = url + '/notes/' + h
            resp = requests.get(u)
            self.assertEqual(resp.status_code, 200)

    def test_acme_req(self):
        url = self.get_server_url()
        u = url + '/.well-known/acme-challenge/token'
        resp = requests.get(u)
        self.assertEqual(resp.status_code, 200)

        u = url + '/.well-known/acme-challenge/foo'
        resp = requests.get(u)
        self.assertEqual(resp.status_code, 404)

    def test_find_key(self):
        token = self.token
        key = self.key
        self.assertEqual(find_key(token), key)

        del os.environ['ACME_TOKEN']
        del os.environ['ACME_KEY']

        os.environ['ACME_TOKEN_ENV'] = token
        os.environ['ACME_KEY_ENV'] = key
        self.assertEqual(find_key(token), key)

        del os.environ['ACME_TOKEN_ENV']
        del os.environ['ACME_KEY_ENV']

    def test_acme(self):
        token = self.token
        key = self.key
        self.assertEqual(acme(token), key)

        token = token + "_env"
        key = key + "_env"
        os.environ['ACME_TOKEN_ENV'] = token
        os.environ['ACME_KEY_ENV'] = key
        self.assertEqual(find_key(token), key)

        del os.environ['ACME_TOKEN_ENV']
        del os.environ['ACME_KEY_ENV']

        self.assertRaises(NotFound, acme, token)

    def test_index_redirection(self):
        resp = index_redirection()
        self.assertEqual(resp.status_code, 200)
        resp.close()

    def test_static_proxy(self):
        htmls = os.listdir(os.path.join(ROOT, 'notes'))

        for h in htmls:
            u = 'notes/' + h
            resp = static_proxy(u)
            self.assertEqual(resp.status_code, 200)
            resp.close()


if __name__ == "__main__":
    unittest.main()
