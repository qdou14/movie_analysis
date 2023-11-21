import requests
import pandas as pd
import seaborn as sns

class APIClient:
    def __init__(self, base_url="http://bechdeltest.com/api/v1"):
        self.base_url = base_url

    def _get_response(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()

    def get_movies_by_title(self, title):
        """Retrieve movies by title."""
        data = self._get_response("getMoviesByTitle", params={"title": title})
        return pd.DataFrame(data)
    
    def get_movie_by_imdb_id(self, imdb_id):
        """Retrieve a single movie by its IMDB ID."""
        data = self._get_response("getMovieByImdbId", params={"imdbid": imdb_id})
        return pd.DataFrame([data]) 

    def get_all_movies(self):
        """Fetch all movies from the API."""
        data = self._get_response("getAllMovies")
        return pd.DataFrame(data)
    
    def process_movies(self, df):
        """Process movie DataFrame with proper labels and types."""
        df.rename(columns={'rating': 'Bechdel Score'}, inplace=True)
        df['year'] = pd.to_datetime(df['year'], format='%Y')
        df_new = df[df['year'] > pd.to_datetime('1967')]
        df_new['Bechdel Score'] = df_new['Bechdel Score'].astype('category', copy=False)
        return df_new

    def plot_bechdel_score(self, df):
        """Plot the Bechdel Score distribution."""
        ax = sns.countplot(x='Bechdel Score', data=df)
        ax.set_xlabel('Bechdel Score')
        ax.set_ylabel('Count')
        return ax.figure

    def add_pass_test_column(self, df):
        """Add a 'pass_test' column to indicate passing the Bechdel test."""
        df['pass_test'] = df['Bechdel Score'].apply(lambda score: 1 if score >= 3 else 0)
        return df
    
    def plot_pass_test(self, df):
        """Plot the distribution of the 'pass_test' column."""
        ax = sns.countplot(x='pass_test', data=df)
        ax.set_xlabel('Pass Bechdel Test')
        ax.set_ylabel('Count')
        return ax.figure