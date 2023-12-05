import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class RottenTomatoesScraper:
    """
    A scraper for Rotten Tomatoes movie ratings.

    This class provides methods to scrape Rotten Tomatoes for movie data and visualize it.

    Attributes
    ----------
    url : str
        The URL of the Rotten Tomatoes page to scrape.

    Methods
    -------
    get_soup():
        Retrieves the webpage from the specified URL and returns a BeautifulSoup object.
        
    scrape_movies():
        Scrapes the Rotten Tomatoes webpage for movies data and returns it as a DataFrame.

    prepare_data(df):
        Prepares and cleans the scraped movie data for analysis.

    plot_number_of_movies_by_year(df):
        Plots a bar chart of the number of movies by year.

    plot_average_score_by_year(df):
        Plots a bar chart of the average movie score by year.
    """

    def __init__(self, url):
        """
        Parameters
        ----------
        url : str
            The URL of the Rotten Tomatoes page to scrape.
        """
        self.url = url

    def get_soup(self):
        """
        Retrieves the webpage from the specified URL.

        Returns
        -------
        BeautifulSoup
            A BeautifulSoup object of the parsed HTML document.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh) '}
        response = requests.get(self.url, headers=headers)
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def scrape_movies(self):
        """
        Scrapes the Rotten Tomatoes webpage for movies data.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the scraped movie data with titles, years, scores, and URLs.
        """
        soup = self.get_soup()
        headings = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
        movies_data = []
        for heading in headings:
            # Extract title, year, score, and URL and clean the text
            title = heading.find("a").text.strip()
            year = heading.find("span", {"class": 'start-year'}).text.strip('()').strip()
            score = heading.find("span", {"class": 'tMeterScore'}).text.strip()
            url = heading.find('a')['href'].strip()
            movies_data.append({
                'title': title,
                'year': year,
                'score': score,
                'url': url
            })
        return pd.DataFrame(movies_data)

    def prepare_data(self, df):
        """
        Prepares and cleans the scraped movie data for analysis.

        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the scraped movie data.

        Returns
        -------
        DataFrame
            The DataFrame with cleaned and formatted data ready for analysis.
        """
        df['score'] = df['score'].str.rstrip('%').astype('float') / 100
        df['year'] = df['year'].astype('int')
        return df

    def plot_number_of_movies_by_year(self, df):
        """
        Plots a bar chart of the number of movies by year.

        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the movie data to be plotted.
        """
        df['year'].value_counts().sort_index().plot(kind='bar', figsize=(10, 5))
        plt.title('Number of Movies by Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Movies')
        plt.tight_layout()
        plt.show()

    def plot_average_score_by_year(self, df):
        """
        Plots a bar chart of the average movie score by year.

        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the movie data with scores to be plotted.
        """
        df.groupby('year')['score'].mean().plot(kind='bar', figsize=(10, 5))
        plt.title('Average Satisfaction by Year')
        plt.xlabel('Year')
        plt.ylabel('Average Score')
        plt.tight_layout()
        plt.show()