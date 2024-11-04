from ingest_mgoblog_data.common.web_scraper import MGoBlogWebScraper

def test_valid_url():
    ws = MGoBlogWebScraper()

    valid_url = "https://www.mgoblog.com/"

    result = ws._get_web_page(url=valid_url)

    assert len(result) > 0

def test_invalid_url_fails():
    ws = MGoBlogWebScraper()

    invalid_url = "https://www.espn.com/junk"

    assert ws._get_web_page(url=invalid_url) == ""

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
    content_links = ws.get_content_links(page_content=sample_html)
    assert len(content_links) == 2
    assert content_links[0] == "right"
    assert content_links[1] == "right"

def test_get_page_content():

    ws = MGoBlogWebScraper()

    sample_html = """
        <html>
            <body>
                <article class="irrelevant class names">
                    <div class="field--name-tags">
                        <div class="field__item">First Tag</div>
                        <div class="field">Second Tag</div>
                        <div class="field__item">Third Tag</div>
                        <div class="__item">Fourth Tag</div>
                    </div>
                    <span class="field--name-uid">Ben Braden</span>
                    <h1 class="not-page-title">
                        Wrong Test Article
                    </h1>
                    <h1 class="page-title other-names">Test Article</h1>
                    <div class="field--name-body other-class-name test_div">
                        <p>Paragraph One</p>
                        <p>Paragraph Two</p>
                    </div>
                    <div class="body">
                        <p>Paragraph Three</p>
                    </div>
                </article>
            </body>
        </html>
    """
    content_data = ws._get_page_content(page_content=sample_html)

    assert content_data['tags'] == ['First Tag', 'Third Tag']
    assert content_data['author'] == "Ben Braden"
    assert content_data['title'] == "Test Article"
    assert "Paragraph One" in content_data["body"]
    assert "Paragraph Two" in content_data["body"]
    assert "Paragraph Three" not in content_data["body"]

def test_get_more_content_link_success():

    ws = MGoBlogWebScraper()

    sample_html = """
                    <html>
                        <body>
                            <div class="more-link">
                                <a href="/more_content"></a>
                            </div>
                        </body>
                    </html>
                    """
    
    more_content_link = ws._get_more_content_link(sample_html)

    assert more_content_link == "/more_content"

def test_get_more_content_link_fail():
    ws = MGoBlogWebScraper()

    sample_html = """
                    <html>
                        <body>
                            <div class="more-link">
                            </div>
                        </body>
                    </html>
                    """
    
    more_content_link = ws._get_more_content_link(sample_html)

    assert more_content_link == None

def test_get_more_content_link_success_next_page():
    ws = MGoBlogWebScraper()

    sample_html = """
                    <html>
                        <body>
                            <li class="pager__item--next">
                                <a href="/more_content"></a>
                            </div>
                        </body>
                    </html>
                    """
    
    more_content_link = ws._get_more_content_link(sample_html)

    assert more_content_link == "/more_content"