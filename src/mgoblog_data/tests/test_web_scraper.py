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

def test_get_content_links():
    ws = MGoBlogWebScraper()

    sample_html = """
                 <html>
                    <body>
                        <div class="title-of-title-wrapper">
                                <a href="wrong">Anchor tag edge case</a>
                            <div class='title-wrapper'>
                                <a href="right"></a>
                            </div>
                        </div>
                        <div class='not-title-wrapper'>
                            <a href="wrong"/>
                        </div>
                        <div class='title-wrapper'>
                            <a href="right"/>
                        </div>
                    </body>
                 </html>
    """
    content_links = ws.get_content_links(url_content=sample_html)
    assert len(content_links) == 2
    assert content_links[0] == "right"
    assert content_links[1] == "right"
