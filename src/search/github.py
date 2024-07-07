from requests import get
from .headers import get_random_agent
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_API_KEY = str(os.environ.get("GITHUB_API_KEY"))


def _request(query: str, num: int):
    """
    Function to make a request to the GitHub API to search for repositories.

    Parameters
    ----------
    query : str
        The query to search for.
    page : int
        The page number of the results.

    Returns
    -------
    requests.models.Response
        The response object from the request.
    """
    url = f"https://api.github.com/search/repositories?q={query}&per_page={num}"
    return get(
        url,
        headers={
            "User-Agent": get_random_agent(),
            "Authorization": f"token {GITHUB_API_KEY}",
        },
    ).json()


def gh_search(query: str, num_results: int = 20):
    """
    Function to search GitHub repositories and return the results.

    Parameters
    ----------
    query : str
        The query to search for.
    num_results : int
        The number of results to return.

    Returns
    -------
    iterable
        A yielded list of tuples containing the repository name, link.
    """
    escaped_query = quote_plus(query)

    try:
        response = _request(escaped_query, num_results)
    except Exception as e:
        print("Github Search Failed")
        print("Error:", e)
        return []
    results = []
    for r in response["items"]:
        name = r["full_name"]
        link = r["html_url"]

        results.append((name, link))

    return results
