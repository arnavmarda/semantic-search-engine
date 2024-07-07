from search.utils import search
from multiprocessing import Pool


def retrieve(query: str, n: int, engines: str, mp: bool):
    """
    Utilizes multiprocessing to retrieve results from multiple search engines.
    """
    if mp:
        map_list = [(query, n, e) for e in engines]
        p = Pool(len(map_list))
        results = p.map_async(search, map_list)
        p.close()
        p.join()
        return results.get()
    else:
        return [search((query, n, e)) for e in engines]


def split_and_retrieve(query: str, n: int, engines: str = "gbsh", mp: bool = False):
    """
    Splits and Parses results to seperate lists for each and every search engine.
    """
    results = retrieve(query, n, engines, mp)
    g_res, b_res, s_res, gh_res = [], [], [], []
    count = 0
    if "g" in engines:
        g_res = results[count]
        count += 1
    if "b" in engines:
        b_res = results[count]
        count += 1
    if "s" in engines:
        s_res = results[count]
        count += 1
    if "h" in engines:
        gh_res = results[count]
        count += 1

    return g_res, b_res, s_res, gh_res
