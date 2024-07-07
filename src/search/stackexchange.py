from .google import g_search


def se_search(query: str, num_results: int = 20, timeout: int = 5):
    """
    Function to search Stack Exchange and return the results.

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
        A yielded list of tuples containing the title and link of the search results.
    """
    try:
        return g_search(query, num_results, timeout, "stackexchange.com")
    except Exception as e:
        print("Stack Exchange Search Failed")
        print("Error:", e)
        return []
