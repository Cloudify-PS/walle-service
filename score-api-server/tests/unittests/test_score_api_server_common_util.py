import unittest
import flask

from score_api_server.common import util


class TestBase(unittest.TestCase):

    def test_add_org_prefix(self):
        app = flask.Flask(__name__)

        with app.app_context():
            flask.g.org_id = "some_id"
            self.assertEqual(
                util.add_org_prefix("magic"),
                "some_id_magic"
            )

if __name__ == '__main__':
    unittest.main()
