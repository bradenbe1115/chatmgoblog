import requests
from bs4 import BeautifulSoup

class WebScraper:

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