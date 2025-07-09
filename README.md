Declare requirements in `goboscript.toml`

```toml
[requirements]
reponame = "username/reponame==1.*.*"
```

Run `backpack` to lock & install them into the `backpack/` directory.

Commit `backpack-lock.json` to version control.

Include library code from the `backpack/` directory.

```
%include backpack/username/reponame/mylibrary
```
