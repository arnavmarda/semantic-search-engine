from requests import get
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .headers import get_random_agent


def _request(query: str, start: int, timeout: int):
    """
    Function to make a request to Bing Search.

    Parameters
    ----------
    query : str
        The query to search for.
    start : int
        The starting index of the results. Results are 1-indexed.
    timeout : int
        The timeout for the request.

    Returns
    -------
    requests.models.Response
        The response object from the request.
    """
    headers = {"User-Agent": get_random_agent()}
    params = {
        "q": query,
        "first": start,
    }
    url = "https://www.bing.com/search"
    return get(url, headers=headers, params=params, timeout=timeout)


def b_search(query: str, num_results: int = 20, timeout: int = 5):
    """
    Function to search Bing and return the results.

    Parameters
    ----------
    query : str
        The query to search for.
    num_results : int
        The number of results to return.
    timeout : int
        The timeout for the request.

    Returns
    -------
    iterable
        A yielded list of tuples containing the title and link snippet of the search results.
    """
    escaped_query = quote_plus(query)
    count = 0
    results = []
    for start in range(1, num_results + 1, 10):
        try:
            response = _request(escaped_query, start, timeout)
        except Exception as e:
            print("Bing Search Failed")
            print("Error:", e)
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        for result in soup.find_all("li", attrs={"class": "b_algo"}):
            title = result.find("h2")
            link = result.find("a", href=True)
            if title and link:
                results.append((title.text, link["href"]))
                count += 1
            if count >= num_results:
                break
        if count >= num_results:
            break

    return results
