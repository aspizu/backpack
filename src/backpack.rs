use std::fs;
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::path::PathBuf;

use anyhow::Context;
use arcstr::ArcStr;
use fxhash::FxHashSet;

pub struct Backpack {
    path: PathBuf,
    packages: FxHashSet<ArcStr>,
}

impl Backpack {
    pub fn new(path: PathBuf) -> anyhow::Result<Self> {
        _ = fs::remove_dir_all(&path);
        fs::create_dir_all(&path).context("Failed to create backpack directory")?;
        let mut file =
            File::create(path.join(".gitignore")).context("Failed to create .gitignore")?;
        file.write_all(b"*\n").unwrap();
        Ok(Self {
            path,
            packages: FxHashSet::default(),
        })
    }

    pub fn add_package(&mut self, name: ArcStr, path: &Path) -> anyhow::Result<()> {
        if self.packages.contains(&name) {
            return Ok(());
        }
        self.packages.insert(name.clone());
        #[cfg(target_os = "windows")]
        std::os::windows::fs::symlink_file(path, self.path.join(&*name))
            .context("Failed to create symlink")?;
        #[cfg(target_os = "linux")]
        std::os::unix::fs::symlink(path, self.path.join(&*name))
            .context("Failed to create symlink")?;
        Ok(())
    }
}
