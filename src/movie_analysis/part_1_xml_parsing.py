import requests
import pandas as pd
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

class XMLName:
    """
    A class used to fetch and parse sitemap data from a website's robots.txt file.
    
    Attributes
    ----------
    base_url : str
        The base URL of the website to fetch the robots.txt from.

    Methods
    -------
    fetch_robots_txt():
        Retrieves the content of the robots.txt file from the base URL.
        
    get_sitemap_data():
        Parses the robots.txt content to extract sitemap URLs and returns a DataFrame.
    """

    def __init__(self, base_url):
        """
        Parameters
        ----------
        base_url : str
            The base URL for fetching the robots.txt file.
        """
        self.base_url = base_url
    
    def fetch_robots_txt(self):
        """
        Retrieves the robots.txt file from the base URL.

        Returns
        -------
        list of str
            A list of sitemap URLs found in the robots.txt file. 
            Returns None if the robots.txt file cannot be retrieved.
        """
        robots_txt_url = urljoin(self.base_url, 'robots.txt')
        try:
            response = requests.get(robots_txt_url)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"robots.txt not found at {robots_txt_url}: {e}")
            return None
        except requests.RequestException as e:
            print(f"Error fetching robots.txt from {robots_txt_url}: {e}")
            return None
        
        sitemap_urls = []
        for line in response.text.splitlines():
            if line.startswith('Sitemap:'):
                sitemap_url = line.split(': ')[1].strip()
                sitemap_urls.append(sitemap_url)
        
        return sitemap_urls
    
    def get_sitemap_data(self):
        """
        Extracts sitemap URLs from the robots.txt file and creates a DataFrame.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the sitemap URLs. 
            If no sitemap URLs are found or robots.txt is missing, returns an empty DataFrame.
        """
        sitemap_urls = self.fetch_robots_txt()
        
        if sitemap_urls is None:
            print("No sitemap data found. Exiting to stay out of jail :)")
            return pd.DataFrame()
            
        sitemap_df = pd.DataFrame({'Sitemap_URLs': sitemap_urls})
        
        return sitemap_df