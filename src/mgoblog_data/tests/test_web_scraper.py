from common.web_scraper import MGoBlogWebScraper
import pytest

def test_valid_url():
    ws = MGoBlogWebScraper()

    valid_url = "https://www.mgoblog.com/"

    result = ws._get_web_page(url=valid_url)

    assert len(result) > 0

def test_invalid_url_fails():
    ws = MGoBlogWebScraper()

    invalid_url = "https://www.espn.com/junk"
    
    with pytest.raises(Exception):
        ws._get_web_page(url=invalid_url)
