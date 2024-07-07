from embeddings.transformers import link_similarity
from multiprocessing import Pool
from halo import Halo
from retrieval import split_and_retrieve
from cli.utils import build_full_table


class SearchResults:
    def __init__(self, query: str, n: int, engines: str, mp: bool):
        self.google = []
        self.bing = []
        self.stackexchange = []
        self.github = []
        self.q = query
        self.n = n
        self.engines = engines
        self.mp = mp
        self.compiled = False

    def build_embedding(self, engine: list):
        if not engine:
            return []
        return [(r[0], r[1], link_similarity(self.q, r[2])) for r in engine]

    def build_embeddings(self):
        if self.mp:
            p = Pool(4)
            results = p.map_async(
                self.build_embedding,
                [self.google, self.bing, self.stackexchange, self.github],
            )
            p.close()
            p.join()
            self.google, self.bing, self.stackexchange, self.github = results.get()
        else:
            self.google = self.build_embedding(self.google)
            self.bing = self.build_embedding(self.bing)
            self.stackexchange = self.build_embedding(self.stackexchange)
            self.github = self.build_embedding(self.github)

    def run(self):
        self.compiled = True
        with Halo(text="Searching and Retrieving Links...", text_color="green"):
            self.google, self.bing, self.stackexchange, self.github = (
                split_and_retrieve(self.q, self.n, self.engines, self.mp)
            )

        with Halo(text="Building Embeddings...", text_color="cyan"):
            self.build_embeddings()

        with Halo(text="Ranking Results...", text_color="yellow"):
            self.rank()

    def rank(self):
        self.google = sorted(self.google, key=lambda x: x[2], reverse=True)
        self.bing = sorted(self.bing, key=lambda x: x[2], reverse=True)
        self.stackexchange = sorted(
            self.stackexchange, key=lambda x: x[2], reverse=True
        )
        self.github = sorted(self.github, key=lambda x: x[2], reverse=True)

    def get_combined_ranking(self):
        results = []
        if len(self.google) != 0:
            results.extend(self.google)
        if len(self.bing) != 0:
            results.extend(self.bing)
        if len(self.stackexchange) != 0:
            results.extend(self.stackexchange)
        if len(self.github) != 0:
            results.extend(self.github)
        return sorted(results, key=lambda x: x[2], reverse=True)

    def get_as_lists(self):
        results = []
        if len(self.google) != 0:
            results.append(self.google)
        if len(self.bing) != 0:
            results.append(self.bing)
        if len(self.stackexchange) != 0:
            results.append(self.stackexchange)
        if len(self.github) != 0:
            results.append(self.github)
        return results

    def build_table(self, show_semantic_score: bool):
        if not self.compiled:
            self.run()

        build_full_table(self.get_as_lists(), self.engines, show_semantic_score)

    def __repr__(self) -> str:
        if self.google:
            print("Google Results:")
            for r in self.google:
                print(f"{r[0]}: {r[1]}")
            print("\n")

        if self.bing:
            print("Bing Results:")
            for r in self.bing:
                print(f"{r[0]}: {r[1]}")
            print("\n")

        if self.stackexchange:
            print("StackExchange Results:")
            for r in self.stackexchange:
                print(f"{r[0]}: {r[1]}")
            print("\n")

        if self.github:
            print("GitHub Results:")
            for r in self.github:
                print(f"{r[0]}: {r[1]}")
            print("\n")

        return ""
