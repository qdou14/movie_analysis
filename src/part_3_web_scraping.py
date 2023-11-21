import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class RottenTomatoesScraper:
    def __init__(self,url):
        self.url = url

    def get_soup(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh) '}
        response = requests.get(self.url, headers=headers)
        print(response.status_code)
        # Using lxml as the parser
        doc1 = BeautifulSoup(response.text, 'html.parser')  
        return doc1

    def scrape_movies(self):
        soup = self.get_soup()
        headings = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
        movies_data = []
        for heading in headings:
            title = heading.find("a").text.strip()  # Added strip() to clean the text
            year = heading.find("span", {"class": 'start-year'}).text.strip('()').strip()  # Clean year text as well
            score = heading.find("span", {"class": 'tMeterScore'}).text.strip()  # Clean score text
            url = heading.find('a')['href'].strip()  # Clean URL as well
            movies_data.append({
                'title': title,
                'year': year,
                'score': score,
                'url': url
            })
        return pd.DataFrame(movies_data)  # Return a DataFrame directly
    
    def prepare_data(self, df):
        # Convert 'score' to numeric and 'year' to integer
        df['score'] = df['score'].str.rstrip('%').astype('float') / 100
        df['year'] = df['year'].astype('int')
        return df

    def plot_number_of_movies_by_year(self, df):
        df['year'].value_counts().sort_index().plot(kind='bar', figsize=(10, 5))
        plt.title('Number of Movies by Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Movies')
        plt.tight_layout()
        plt.show()

    def plot_average_score_by_year(self, df):
        df.groupby('year')['score'].mean().plot(kind='bar', figsize=(10, 5))
        plt.title('Average Satisfaction by Year')
        plt.xlabel('Year')
        plt.ylabel('Average Score')
        plt.tight_layout()
        plt.show()