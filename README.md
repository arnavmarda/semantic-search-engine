# Semantic Search Engine

This package provides a smarter (albeit slower) way to search for information on the internet. It currently supports searching on Google, Bing, Github and Stackexchange. The search results are ranked based on their semantic similarity to the search query. 

## Installation

The only installation supported as of now is through github. You can install the package by cloning into it and then setting up the development environment. To clone the repository, run the following command:

```bash
git clone https://github.com/arnavmarda/semantic-search-engine.git
```

The most efficient way to set up the development environment is by using a virtual environment. The fastest library for installation and setting up the environment is `uv` by astral.sh. You can install it by running the following command:

```bash
pip install uv
```

After installing `uv`, you can set up the development environment by running the following command:

```bash
uv venv
```

Then you can activate the virtual environment by running the following command:

```bash
# For macOS and Linux
source .venv/bin/activate

# For Windows
.venv\Scripts\activate
```

After activating the virtual environment, you can install the dependencies by running the following command:

```bash
uv pip install -r requirements.txt
```

## Usage
The package currently offers 2 ways to run it. 

### Interactive Mode
You can run the package in interactive mode by running the following command:

```bash
python -m src/app.py
# OR
python -m src/app.py inter
```
This will prompt the user for the necessary and information and then display the results in the terminal.

### Command Line Mode
You can run the package in command line mode by running the following command:

```bash
python -m src/app.py ni [COMMANDS] [OPTIONS]
```

The help command can be used to get more information about the commands and options available:

```bash
python -m src/app.py ni --help
```

For reference, the above command will display the following output:

```bash
 Usage: app.py ni [OPTIONS] QUERY

 Non-interactive mode for the CLI.
 The CLI will run with the arguments provided. The arguments are: - query (str): The query to search for. Required. -
 num_results (int): The number of results to retrieve. Optional. Defaults to 10. - engines (str): The search engines to
 use. Optional. Defaults to "gbsh". - multiprocessing (bool): Whether to use multiprocessing. Optional. Defaults to
 False.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    query      TEXT  The query to search for. [default: None] [required]                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --num-results        INTEGER  Number of results to search for. [default: 10]                                           │
│ --engines            TEXT     The different engines to use. [default: gbsh]                                            │
│ --mp                          Enable or Disable multiprocessing.                                                       │
│ --ss                          Show semantic scores in results. [default: True]                                         │
│ --help                        Show this message and exit.                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Future Work
The package is still in its early stages and there is a lot of work to be done. Some of the future work includes:
 - Adding a research mode with Arxiv and Google Scholar support
 - Adding support for other search engines and websites
 - Adding caching to speed up the search process
 - Adding a GUI for the package
 - Adding support for multiple queries at once which will improve the search results