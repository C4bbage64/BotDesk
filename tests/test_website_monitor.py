import unittest
from unittest.mock import patch
from automations.website_monitor import check_website

class TestWebsiteMonitor(unittest.TestCase):
    @patch('automations.website_monitor.requests.get')
    def test_website_online(self, mock_get):
        # Setup mock
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        
        # Run
        result = check_website("google.com")
        
        # Verify
        self.assertEqual(result['status'], 'Online')
        self.assertEqual(result['response_code'], 200)

    @patch('automations.website_monitor.requests.get')
    def test_website_error(self, mock_get):
        # Setup mock
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        
        # Run
        result = check_website("google.com/nothing")
        
        # Verify
        self.assertIn('Error', result['status'])
        self.assertEqual(result['response_code'], 404)

if __name__ == '__main__':
    unittest.main()
