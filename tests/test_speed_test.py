import unittest
from unittest.mock import patch, MagicMock
from automations.speed_test import run_speed_test

class TestSpeedTest(unittest.TestCase):
    @patch('automations.speed_test.speedtest.Speedtest')
    def test_speed_test_success(self, MockSpeedtest):
        # Setup mock
        mock_instance = MockSpeedtest.return_value
        mock_instance.get_best_server.return_value = {}
        mock_instance.download.return_value = 50_000_000 # 50 Mbps
        mock_instance.upload.return_value = 10_000_000   # 10 Mbps
        mock_instance.results.ping = 25.5
        
        # Run function
        result = run_speed_test()
        
        # Verify
        self.assertEqual(result['download'], 50.0)
        self.assertEqual(result['upload'], 10.0)
        self.assertEqual(result['ping'], 25.5)

    @patch('automations.speed_test.speedtest.Speedtest')
    def test_speed_test_failure(self, MockSpeedtest):
        # Setup mock to raise exception
        MockSpeedtest.side_effect = Exception("Connection Error")
        
        # Verify exception
        with self.assertRaises(Exception) as context:
            run_speed_test()
        
        self.assertIn("Speed test failed: Connection Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
