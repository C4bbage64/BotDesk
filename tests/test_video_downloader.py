import unittest
from unittest.mock import patch, MagicMock
from automations.video_downloader import download_video

class TestVideoDownloader(unittest.TestCase):
    @patch('automations.video_downloader.yt_dlp.YoutubeDL')
    def test_download_success(self, MockYoutubeDL):
        # Setup mock
        mock_instance = MockYoutubeDL.return_value
        mock_instance.__enter__.return_value = mock_instance
        
        # Run function
        result = download_video("http://youtube.com/watch?v=123", "output_dir")
        
        # Verify
        self.assertEqual(result, "Download completed successfully.")
        mock_instance.download.assert_called_once_with(["http://youtube.com/watch?v=123"])

    @patch('automations.video_downloader.yt_dlp.YoutubeDL')
    def test_download_failure(self, MockYoutubeDL):
        # Setup mock to raise exception
        mock_instance = MockYoutubeDL.return_value
        mock_instance.__enter__.return_value = mock_instance
        mock_instance.download.side_effect = Exception("Download error")
        
        # Verify exception
        with self.assertRaises(Exception) as context:
            download_video("bad_url", "output_dir")
        
        self.assertIn("Download failed: Download error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
