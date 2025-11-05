import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class BasicTestCase(unittest.TestCase):

    def test_home(self):
        """Test the status endpoint."""
        tester = app.test_client(self)
        response = tester.get('/status', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
