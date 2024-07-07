import typer
from typing_extensions import Annotated
from results import SearchResults
from cli.utils import print_logo, collect_options


app = typer.Typer()


def make_app(
    query: str,
    num_results: int,
    engines: str,
    multiprocessing: bool,
    show_semantic_scores: bool,
):
    s = SearchResults(query, num_results, engines, multiprocessing)
    s.build_table(show_semantic_scores)


@app.command("inter")
def interactive():
    """
    Interactive mode for the CLI.

    The CLI will prompt the user for input. No arguments are required.
    """
    print_logo()
    args = collect_options()
    make_app(
        args["query"],
        args["num_results"],
        args["engines"],
        args["multiprocessing"],
        args["semantic_score"],
    )


@app.command("ni")
def non_interactive(
    query: Annotated[str, typer.Argument(help="The query to search for.")],
    num_results: Annotated[
        int, typer.Option(help="Number of results to search for.")
    ] = 10,
    engines: Annotated[
        str, typer.Option(help="The different engines to use.")
    ] = "gbsh",
    multiprocessing: Annotated[
        bool, typer.Option("--mp", help="Enable or Disable multiprocessing.")
    ] = False,
    show_semantic_scores: Annotated[
        bool, typer.Option("--ss", help="Show semantic scores in results.")
    ] = True,
):
    """
    Non-interactive mode for the CLI.

    The CLI will run with the arguments provided. The arguments are:
    - query (str): The query to search for. Required.
    - num_results (int): The number of results to retrieve. Optional. Defaults to 10.
    - engines (str): The search engines to use. Optional. Defaults to "gbsh".
    - multiprocessing (bool): Whether to use multiprocessing. Optional. Defaults to False.
    """
    print_logo()
    make_app(query, num_results, engines, multiprocessing, show_semantic_scores)


@app.command("gui")
def gui():
    """
    Yet to be implemented.
    """
    raise NotImplementedError("GUI not implemented yet.")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Welcome to the Semantic Search Engine CLI.

    This CLI allows you to search for information across multiple search engines and rank the results based on semantic similarity.

    Use the --help flag to get more information on the available commands.

    Runing the CLI without any arguments will run the interactive mode.

    Enjoy!
    """
    if ctx.invoked_subcommand is None:
        interactive()


if __name__ == "__main__":
    app()
