import requests
import time
from bs4 import BeautifulSoup
from ingest_mgoblog_data.common.models import MgoblogContentLandingDataSchema


class MGoBlogWebScraper:
    site_root = "https://www.mgoblog.com"

    def _get_web_page(self, url: str) -> str:
        """
            Retrieves the web page at the given url and returns the text content of the page.

            If web page cannot be reached, function will return an empty string.

            Args:
                url (str): URL of a web page.
        """
        r = requests.get(url)

        if r.status_code == 200:

            return r.text
        
        else:
            return ""
        
    def get_content_links(self, page_content: str) -> list[str]:
        """
            Parses a list of content links from a MGoBlog web page.

            Args:
                page_content (str): HTML of page that content links will be parsed from
            
            Returns:
                list[str]: list of links to content pages found on web page
        """

        soup = BeautifulSoup(page_content, 'html.parser')

        content_links = []
        title_divs = soup.find_all("div", class_="title-wrapper")

        if title_divs is None:
            return content_links

        for title_div in title_divs:
            anchor_tag = title_div.find("a")

            if anchor_tag:
                content_links.append(anchor_tag["href"])
    
        return content_links
    
    def _get_more_content_link(self, page_content: str) -> str:
        """
            Gets link to more content from page. 
            
            There are two page patterns that we are looking for.

            1) A more articles button located on the bottom of the page

            2) A list with links to numbered pages with a next button at the end.

            Function will look for one of the two buttons for a link to more content and return the link if it's found

            Args:
                page_contant (str): HTML of page to extract link to more content from
            
            Returns:
                str: link to more content. Will return None if no such link is found
        """
        soup = BeautifulSoup(page_content, 'html.parser')
        next_page_li = soup.find("li", class_="pager__item--next")

        try:
            anchor_tag  = next_page_li.find("a")
            return anchor_tag["href"]
        except:
            return None

    def extract_page_data(self, page_content: str) -> dict:
        """
            Extracts data from the HTML of a MGoBlog content page.

            Function will find the following fields in the html and return within a dictionary:
            - tags
            - title
            - author
            - date written
            - body (text of the body of the page's content)

            Args:
                page_content (str): HTML of page to extract content data from

            Returns:
                dict: content data to return from page
        """

        soup = BeautifulSoup(page_content, 'html.parser')

        article = soup.find("article")

        if article is None:
            return {}

        # Extract article tags
        tags = []
        try:
            tag_div_items = article.find("div",class_="field--name-tags").find_all("div", class_="field__item")
            for tag_div_item in tag_div_items:
                tags.append(tag_div_item.text)
        
        except:
            pass # If tag divs not found, do nothing

        # Extract author
        author_div = article.find("span", class_="field--name-uid")
        if author_div is not None:
            author = author_div.text.strip()
        else:
            author = None

        # Extract date written
        author_date_div = article.find("div", class_="node__meta")
        author_date_text = author_date_div.text 
        if author is not None:
            date_written = author_date_text.replace(author, "").strip()
        else:
            date_written = author_date_text.strip()

        # Extract page title
        title_header = article.find("h1", class_="page-title")
        if title_header is not None:
            title = title_header.text.strip()
        else:
            title = None

        # Extract page body content
        body_div = article.find("div", class_="field--name-body")
        if body_div is not None:
            body = body_div.get_text(separator=" ", strip=True)
        else:
            body = None

        return {"tags": tags, "title": title, "author": author, "body": body, "date_written": date_written}
    
    def get_content(self, start_url: str, max_iteration: int=5, iteration: int=0, results: list[dict]=None) -> list[MgoblogContentLandingDataSchema]:
        """
            Finds links to content on Mgoblog page, gets content data from links, and recursively iterates process to next page.

            Args:
                start_url (str): Initial page to start scraping content from
                max_iterations (int): Max number of pages to look for content on
                iteration (int): Number of pages iterated through
        """

        if results is None:
            results = []

        if iteration == max_iteration:
            return results
        
        start_page_content = self._get_web_page(url=f"{start_url}?page={iteration+1}")

        if len(start_page_content) == 0:
            return results

        content_links = self.get_content_links(page_content=start_page_content)

        # Iterate through content pages one by one and retrieve data
        for content_link in content_links:
            full_content_url = f"{self.site_root}{content_link}"
            print(full_content_url)
            web_page_html = self._get_web_page(url=full_content_url)

            if len(web_page_html) > 0:
                results.append(MgoblogContentLandingDataSchema(url=full_content_url, raw_html=web_page_html, collected_ts=int(time.time())))
        
        else:
            return self.get_content(start_url=start_url, max_iteration=max_iteration, iteration=iteration+1, results=results)
        



