from requests import get
from bs4 import BeautifulSoup
from .headers import get_random_agent
from bs4.element import Comment
from .bing import b_search
from .github import gh_search
from .google import g_search

# from .stackexchange import se_search
# from random import sample
# from math import ceil


def filter_text(element):
    """
    Function to filter out non-text elements from the HTML.
    """
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False

    if len(element.strip()) < 25:
        return False

    return True


def _get_all_text(link: str):
    """
    Sends a GET request to the link and retrieves all human-readable and copyable text from the page.
    """
    response = get(link, headers={"User-Agent": get_random_agent()})
    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.find_all(text=True)
    filtered_texts = list(map(lambda x: x.strip(), filter(filter_text, texts)))
    return filtered_texts


def search(packed_args: tuple):
    """
    Searches the query on the specified search engine and retrieves the top n results.
    """
    query, n, engine = packed_args
    res = None
    if engine == "g":
        res = g_search(query, n)
    elif engine == "b":
        res = b_search(query, n)
    elif engine == "s":
        res = g_search(query, n, site="stackexchange.com")
    elif engine == "h":
        res = gh_search(query, n)
    else:
        raise ValueError("Invalid Engine Specified!")

    return [(r[0], r[1], _get_all_text(r[1])) for r in res]
