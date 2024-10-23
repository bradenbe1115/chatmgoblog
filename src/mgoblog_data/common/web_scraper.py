import requests
from bs4 import BeautifulSoup

class MGoBlogWebScraper:

    def _get_web_page(self, url: str) -> str:
        """
            Retrieves the web page at the given url and returns the text content of the page.

            If web page cannot be reached, function will throw an exception.

            Args:
                url (str): URL of a web page.
        """
        r = requests.get(url)

        if r.status_code == 200:

            return r.text
        
        else:
            raise Exception(f"Error in accessing web page. Received status code {r.status_code}.")
        
    def get_content_links(self, url_content: str) -> list[str]:
        """
            Parses a list of content links from a MGoBlog web page.

            Args:
                url_content (str): Content of an MGoBlog page in a str
            
            Returns:
                list[str]: list of links to content pages found on web page
        """
        soup = BeautifulSoup(url_content, 'html.parser')

        content_links = []
        title_divs = soup.find_all("div", class_="title-wrapper")
        for title_div in title_divs:
            anchor_tag = title_div.find("a")

            if anchor_tag:
                content_links.append(anchor_tag["href"])
    
        return content_links

