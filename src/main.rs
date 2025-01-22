mod backpack;
mod cli;
mod frontend;
mod manifest;
mod misc;
mod package;
mod packages_cache;
mod project;

use std::time::Instant;

use colored::Colorize;

fn main() -> anyhow::Result<()> {
    std::panic::set_hook(Box::new(|info| {
        eprintln!(
            "{info}\n{}\nopen an issue at {}",
            "-9999 aura 💀".red().bold(),
            "https://github.com/aspizu/backpack/issues".cyan()
        );
    }));
    let begin = Instant::now();
    let result = frontend::frontend();
    eprintln!("{} in {:?}", "Finished".green().bold(), begin.elapsed());
    result
}
