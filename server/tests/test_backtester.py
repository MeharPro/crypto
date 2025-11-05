import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class BacktesterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('backtester.tradeapi.REST')
    def test_backtest_endpoint(self, mock_rest):
        """Test the /backtest endpoint."""
        # Mock the Alpaca API client
        mock_api_instance = MagicMock()
        mock_rest.return_value = mock_api_instance

        # Mock the return value of get_bars to simulate historical data
        mock_api_instance.get_bars.return_value.df = MagicMock()

        # Mock the run method of the Backtester class
        with patch('app.Backtester.run') as mock_run:
            mock_run.return_value = {"status": "success", "profit_loss": 1234.56}

            response = self.app.post('/backtest',
                                     json={
                                         "symbol": "AAPL",
                                         "startDate": "2022-01-01",
                                         "endDate": "2023-01-01"
                                     })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['profit_loss'], 1234.56)

if __name__ == '__main__':
    unittest.main()
