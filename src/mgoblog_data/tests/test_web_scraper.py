from common.web_scraper import WebScraper
import pytest

def test_valid_url():
    ws = WebScraper()

    valid_url = "https://www.mgoblog.com/"

    result = ws._get_web_page(url=valid_url)

    assert len(result) > 0

def test_invalid_url_fails():
    ws = WebScraper()

    invalid_url = "https://www.espn.com/junk"
    
    with pytest.raises(Exception):
        ws._get_web_page(url=invalid_url)
