use std::env::current_dir;
use std::path::PathBuf;
use std::sync::Arc;
use std::sync::Mutex;

use clap::CommandFactory;
use clap::Parser;
use directories::ProjectDirs;

use crate::cli::Cli;
use crate::cli::Command;
use crate::package::Package;
use crate::packages_cache::PackagesCache;
use crate::project::Project;

fn sync(packages_cache: Arc<Mutex<PackagesCache>>, input: Option<PathBuf>) -> anyhow::Result<()> {
    let input = input.unwrap_or_else(|| current_dir().unwrap());
    let package = Package::new(input.clone())?;
    let mut project = Project::new(input, packages_cache.clone())?;
    project.add_dependencies_for_package(&package)
}

pub fn frontend() -> anyhow::Result<()> {
    let command = Cli::parse().command;
    if let Command::Completions { shell } = command {
        shell.generate(&mut Cli::command(), &mut std::io::stdout());
        return Ok(());
    }
    let directories = ProjectDirs::from("com", "aspizu", "backpack").unwrap();
    let packages_cache = Arc::new(Mutex::new(PackagesCache::new(
        directories.cache_dir().join("packages"),
    )?));
    match command {
        Command::Sync { input } => sync(packages_cache, input),
        Command::Purge { all } => {
            if all {
                packages_cache.lock().unwrap().purge_all()
            } else {
                packages_cache.lock().unwrap().purge()
            }
        }
        Command::Completions { .. } => unreachable!(),
    }
}
