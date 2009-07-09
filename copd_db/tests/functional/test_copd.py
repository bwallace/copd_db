from copd_db.tests import *

class TestCopdController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='copd'))
        # Test response...
