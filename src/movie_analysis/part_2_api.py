import requests
import pandas as pd
import seaborn as sns

class APIClient:
    """
    A client for interacting with a web API to retrieve and process movie data.
    
    Attributes:
    base_url (str): The base URL of the API.

    Methods:
    __init__(self, base_url): Initializes the API client with a base URL.
    _get_response(self, endpoint, params=None): Sends a GET request to an API endpoint.
    get_movies_by_title(self, title): Retrieves movies by their title.
    get_movie_by_imdb_id(self, imdb_id): Retrieves a single movie by its IMDB ID.
    get_all_movies(self): Fetches all movies from the API.
    process_movies(self, df): Processes a DataFrame of movies.
    plot_bechdel_score(self, df): Plots the distribution of Bechdel Scores.
    add_pass_test_column(self, df): Adds a column indicating if a movie passes the Bechdel test.
    plot_pass_test(self, df): Plots the distribution of movies passing/failing the Bechdel test.
    """

    def __init__(self, base_url):
        """
        Initialize the API client with a base URL.

        Parameters:
        base_url (str): The base URL for the API endpoints.
        """
        self.base_url = base_url

    def _get_response(self, endpoint, params=None):
        """
        Send a GET request to a specific endpoint and return the JSON response.

        Parameters:
        endpoint (str): The API endpoint to send the request to.
        params (dict, optional): A dictionary of parameters to be sent with the request.

        Returns:
        dict: The JSON response from the API.

        Raises:
        HTTPError: If the HTTP request returns an unsuccessful status code.
        """
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_movies_by_title(self, title):
        """
        Retrieve movies by their title.

        Parameters:
        title (str): The title of the movies to retrieve.

        Returns:
        DataFrame: A pandas DataFrame containing the retrieved movies.
        """
        data = self._get_response("getMoviesByTitle", params={"title": title})
        return pd.DataFrame(data)
    
    def get_movie_by_imdb_id(self, imdb_id):
        """
        Retrieve a single movie by its IMDB ID.

        Parameters:
        imdb_id (str): The IMDB ID of the movie to retrieve.

        Returns:
        DataFrame: A pandas DataFrame containing the retrieved movie.
        """
        data = self._get_response("getMovieByImdbId", params={"imdbid": imdb_id})
        return pd.DataFrame([data]) 

    def get_all_movies(self):
        """
        Fetch all movies from the API.

        Returns:
        DataFrame: A pandas DataFrame containing all the movies.
        """
        data = self._get_response("getAllMovies")
        return pd.DataFrame(data)
    
    def process_movies(self, df):
        """
        Process a DataFrame of movies to apply proper labels, types, and filtering.

        Parameters:
        df (DataFrame): The DataFrame of movies to process.

        Returns:
        DataFrame: The processed DataFrame.
        """
        df = df.rename(columns={'rating': 'Bechdel Score'})
        df = df[pd.to_datetime(df['year'], format='%Y') > pd.to_datetime('1967')]
        df = df.assign(Bechdel_Score=lambda x: x['Bechdel Score'].astype('category'))
        return df

    def plot_bechdel_score(self, df):
        """
        Plot the distribution of Bechdel Scores in the provided DataFrame.

        Parameters:
        df (DataFrame): The DataFrame containing movie data with Bechdel Scores.

        Returns:
        Figure: The matplotlib figure object for the plot.
        """
        ax = sns.countplot(x='Bechdel Score', data=df)
        ax.set_xlabel('Bechdel Score')
        ax.set_ylabel('Count')
        return ax.figure

    def add_pass_test_column(self, df):
        """
        Add a column to the DataFrame indicating whether each movie passes the Bechdel test.

        Parameters:
        df (DataFrame): The DataFrame to which the column will be added.

        Returns:
        DataFrame: The DataFrame with the new 'pass_test' column.
        """
        df['pass_test'] = df['Bechdel Score'].apply(lambda score: 1 if score >= 3 else 0)
        return df
    
    def plot_pass_test(self, df):
        """
        Plot the distribution of movies that pass or fail the Bechdel test.

        Parameters:
        df (DataFrame): The DataFrame containing movie data with Bechdel Scores.

        Returns:
        Figure: The matplotlib figure object for the plot.
        """
        ax = sns.countplot(x='pass_test', data=df)
        ax.set_xlabel('Pass Bechdel Test')
        ax.set_ylabel('Count')
        return ax.figure