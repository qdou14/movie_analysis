import requests
import pandas as pd
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

class XMLname:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def fetch_robots_txt(self):
        try:
            response = requests.get(urljoin(self.base_url, 'robots.txt'))
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            print(f"Error fetching robots.txt: {e}")
            return []
        
        sitemap_urls = []
        for line in response.text.splitlines():
            if line.startswith('Sitemap:'):
                sitemap_url = line.split(': ')[1].strip()
                sitemap_urls.append(sitemap_url)
        
        return sitemap_urls
    
    def get_sitemap_data(self):
        # Get sitemap URLs
        sitemap_urls = self.fetch_robots_txt()
        
        # Create a DataFrame
        sitemap_df = pd.DataFrame({'Sitemap_URLs': sitemap_urls})
        
        return sitemap_df