# `backpack`

backpack is the goboscript package manager.

## Usage

```
usage: backpack <command>

     sync <path>    Synchronizes the project's dependencies
                    path: The path to the project's root directory. (Default: current directory)
     purge          Removes unused packages from the cache
```

### Manifest

List the dependencies of your package in the `goboscript.toml` file.

```toml
[dependencies]
packageName = "https://github.com/author/packageName@v1.0.0"
```

`v1.0.0` is a git tag.

### Sync

Download and link all the files from the dependencies recursively
inside the `backpack` directory in your package's root directory.

Use the dependencies in your package by `%include`ing them from the `backpack` directory.

```goboscript
%include backpack/packageName/packageFile
```

### Purge

Remove unused packages from the cache (located in `~/.backpack/cache/packages`).

