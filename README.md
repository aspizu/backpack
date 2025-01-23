# `backpack`

backpack is the package manager for [goboscript](https://github.com/aspizu/goboscript).

backpack fetches and places all dependencies inside the `backpack` directory in your
project. backpack allows you to specify dependencies inside `goboscript.toml` by their
git repository URL and tag name (version).

## Installation

```shell
git clone https://github.com/aspizu/backpack
cd backpack
cargo install --path .
```

## Usage

```
Usage: backpack <COMMAND>

Commands:
  sync         Fetch and add dependencies to the backpack directory
  purge        Purge unused packages from the package cache
  completions  
  help         Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

## Getting Started

Add dependencies to your project by adding them to `goboscript.toml`:

```toml
[dependencies]
dependencyName = "https://github.com/aspizu/dependencyName@v1.0.0"
```

Then run `backpack sync` to fetch and add the dependencies to the backpack directory.

backpack will recursively add all dependencies to the backpack directory.

## Purging the Package Cache

backpack caches cloned git repositories in the user cache directory, you can choose to
either remove cached packages which haven't been used for 30 days or all cached
packages.

To remove unused packages run `backpack purge --all` or `backpack purge`.
