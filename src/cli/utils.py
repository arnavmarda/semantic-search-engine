# Text Box for Query
# Text Box for Num Results
# Checkboxes for Search Engines
# Flag for Multiprocessing
# Button to Run Search

# Tabular Display of Results
import inquirer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.align import Align

from pyfiglet import Figlet


def table_layout(engines: str):
    if len(engines) == 1:
        return [1]
    if len(engines) == 2:
        return [2]
    if len(engines) == 3:
        return [2, 1]
    if len(engines) == 4:
        return [2, 2]
    raise ValueError("Invalid number of engines")


def print_logo():
    f = Figlet(font="larry3d")
    rprint(f"[bold spring_green2]{f.renderText('Semantic Search Engine')}")


def collect_options():
    questions = [
        inquirer.Text("query", message="Enter your query"),
        inquirer.Text(
            "num_results",
            message="Enter the number of results to retrieve",
            default="10",
            validate=lambda _, x: x.isdigit(),
        ),
        inquirer.Checkbox(
            "engines",
            message="Select the search engines you want to use",
            choices=["google", "bing", "stackexchange", "github"],
        ),
        inquirer.Confirm(
            "multiprocessing", message="Use multiprocessing?", default=False
        ),
        inquirer.Confirm(
            "semantic_score",
            message="Show semantic scores in the results?",
            default=True,
        ),
    ]
    answers = inquirer.prompt(questions)
    lookup = {"github": "h", "google": "g", "bing": "b", "stackexchange": "s"}
    engines = answers["engines"]
    for i, engine in enumerate(engines):
        engines[i] = lookup[engine]
    answers["engines"] = "".join(engines)
    answers["num_results"] = int(answers["num_results"])
    return answers


def results_table(
    engine_results: list[tuple],
    show_semantic_score: bool = False,
    show_edge: bool = False,
) -> Table:
    table = Table(show_edge=show_edge, show_lines=True)
    table.add_column("#", style="bright_black", justify="center", header_style="bold")
    table.add_column(
        "Title",
        style="bright_cyan",
        justify="left",
        header_style="bold",
        overflow="fold",
    )
    table.add_column(
        "Link",
        style="bright_yellow",
        justify="left",
        header_style="bold",
        overflow="ellipsis",
    )
    if show_semantic_score:
        table.add_column(
            "Semantic Score", style="bright_red", justify="center", header_style="bold"
        )

    for i, result in enumerate(engine_results):
        if show_semantic_score:
            table.add_row(str(i + 1), result[0], result[1], str(result[2]))
        else:
            table.add_row(str(i + 1), result[0], result[1])

    return table


def build_full_table(results: list, engines: str, show_semantic_score: bool = False):
    engine_lookup = {"g": "Google", "b": "Bing", "s": "StackExchange", "h": "GitHub"}
    engines_list = [engine_lookup[engine] for engine in engines]
    layout = table_layout(engines)
    console = Console()
    console.rule("[bold red]Categorized Search Results")
    added = 0
    for n in layout:
        table = Table(show_lines=True)
        for i in range(n):
            table.add_column(
                engines_list[added + i], justify="center", header_style="bold"
            )
        table.add_row(
            *[results_table(results[added + i], show_semantic_score) for i in range(n)]
        )
        table = Align.center(table, vertical="middle")
        console.print(table)
        added += n

    console.rule("[bold red]Combined Search Results")

    combined_results = []
    for engine in results:
        combined_results.extend(engine)
    combined_results = sorted(combined_results, key=lambda x: x[2], reverse=True)
    console.print(
        Align.center(
            results_table(combined_results, show_semantic_score, show_edge=True),
            vertical="middle",
        )
    )
