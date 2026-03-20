Backpack is a simple package manager that works like [`cargo`](https://doc.rust-lang.org/cargo/guide/dependencies.html) or [`uv`](https://docs.astral.sh/uv/concepts/projects/dependencies/).

---

Declare requirements in `goboscript.toml`

```toml
[requirements]
reponame = "username/reponame==1.*.*"
```

Run `backpack` to lock & install them into the `backpack/` directory.

Commit `backpack-lock.json` to version control. This file stores the versions of the packages.

Include library code from the `backpack/` directory.

```
%include backpack/username/reponame/mylibrary
```
