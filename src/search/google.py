from bs4 import BeautifulSoup
from requests import get
from .headers import get_random_agent
from urllib.parse import quote_plus


def _request(query: str, num_results: int, start: int, timeout: int, site: str):
    """
    Function to make a request to Google Search.

    Parameters
    ----------
    query : str
        The query to search for.
    num_results : int
        The number of results to return.
    start : int
        The starting index of the results.
    timeout : int
        The timeout for the request.

    Returns
    -------
    requests.models.Response
        The response object from the request.
    """
    headers = {
        "User-Agent": get_random_agent(),
    }
    params = {
        "q": f"{query} site:{site}",
        "num": num_results,
        "start": start,
    }
    url = "https://www.google.com/search"
    response = get(url, headers=headers, params=params, timeout=timeout)
    return response


def g_search(query: str, num_results: int = 20, timeout: int = 5, site: str = ""):
    """
    Function to search Google and return the results.

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
    while count < num_results:
        try:
            response = _request(escaped_query, num_results, count, timeout, site)
        except Exception as e:
            print("Google Search Failed")
            print("Error:", e)
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        blocks = soup.find_all("div", attrs={"class": "g"})

        for block in blocks:
            link = block.find("a", href=True)["href"]
            title = block.find("h3")
            if link and title and count < num_results:
                count += 1
                results.append((title.text, link))

        if count == 0:
            return []

    return results
