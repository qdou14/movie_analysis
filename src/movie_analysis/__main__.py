"""Enable running `python -m project_package` to analyze movie data from various sources."""
import matplotlib.pyplot as plt

from .part_1_xml_parsing import XMLName
from .part_2_api import APIClient
from .part_3_web_scraping import RottenTomatoesScraper

def main():
    """
    Run movie data analysis as a script, processing and visualizing
    data from XML, APIs, and web scraping.
    """
    print("------------------------------------------------")
    print("Project_2_Movie_Analysis")
    print("------------------------------------------------")
    part1()
    print("------------------------------------------------")
    part2()
    print("------------------------------------------------")
    part3_and_part4()
    print("------------------------------------------------")


def part1():
    """Parse XML sitemap data."""
    xmlname = XMLName("https://www.fandango.com/")
    sitemap_data = xmlname.get_sitemap_data()
    print(sitemap_data)


def part2():
    """Fetch movie data from an API."""
    api_client = APIClient(base_url="http://bechdeltest.com/api/v1")
    df_all_movies = api_client.get_all_movies()
    print(df_all_movies.head())

    df_movies_by_title = api_client.get_movies_by_title("matrix")
    print(df_movies_by_title.head())

    imdb_id = "0133093"
    df_movie_by_imdb = api_client.get_movie_by_imdb_id(imdb_id)
    print(df_movie_by_imdb.head())


def part3_and_part4():
    """Scrape movie data from Rotten Tomatoes and perform further analysis."""
    scraper = RottenTomatoesScraper("https://editorial.rottentomatoes.com/guide/golden-globes-best-film-winners-by-tomatometer/")
    movies_df = scraper.scrape_movies()
    print(movies_df.head())

    # Perform additional analysis and visualization for Part 4 using the same scraped data
    df_processed = scraper.prepare_data(movies_df)
    scraper.plot_number_of_movies_by_year(df_processed)
    scraper.plot_average_score_by_year(df_processed)

    # Assuming the APIClient class has the following methods for analysis
    api_client = APIClient(base_url="http://bechdeltest.com/api/v1")
    df_all_movies = api_client.get_all_movies()
    df_processed = api_client.process_movies(df_all_movies)
    df_processed = api_client.add_pass_test_column(df_processed)

    # Plot and display figures
    api_client.plot_bechdel_score(df_processed)
    api_client.plot_pass_test(df_processed)
    plt.show() 


if __name__ == "__main__":
    main()