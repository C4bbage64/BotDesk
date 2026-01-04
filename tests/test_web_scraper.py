import unittest
from unittest.mock import patch, MagicMock
from automations.web_scraper import scrape_website

class TestWebScraper(unittest.TestCase):
    @patch('automations.web_scraper.requests.get')
    def test_scrape_links(self, mock_get):
        # Setup mock HTML
        html_content = """
        <html>
            <body>
                <a href="/page1">Link 1</a>
                <a href="https://example.com/page2">Link 2</a>
            </body>
        </html>
        """
        mock_response = mock_get.return_value
        mock_response.text = html_content
        mock_response.raise_for_status = MagicMock()
        
        # Run
        results = scrape_website("https://example.com", target='links')
        
        # Verify
        self.assertEqual(len(results), 2)
        self.assertIn("https://example.com/page1", results)

    @patch('automations.web_scraper.requests.get')
    def test_scrape_text(self, mock_get):
        # Setup mock HTML
        html_content = """
        <html>
            <body>
                <h1>Header</h1>
                <p>Paragraph text.</p>
            </body>
        </html>
        """
        mock_response = mock_get.return_value
        mock_response.text = html_content
        
        # Run
        results = scrape_website("https://example.com", target='text')
        
        # Verify
        self.assertEqual(len(results), 2)
        self.assertIn("Header", results)
        self.assertIn("Paragraph text.", results)

if __name__ == '__main__':
    unittest.main()
