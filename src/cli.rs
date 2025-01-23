use std::path::PathBuf;

use clap_derive::Parser;
use clap_derive::Subcommand;

#[derive(Debug, Parser)]
#[command(
    version = env!("CARGO_PKG_VERSION"),
    author = env!("CARGO_PKG_AUTHORS"),
    about = env!("CARGO_PKG_DESCRIPTION"),
    long_about = env!("CARGO_PKG_DESCRIPTION"),
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Fetch and add dependencies to the backpack directory.
    #[command()]
    Sync { input: Option<PathBuf> },
    /// Purge unused packages from the package cache.
    #[command()]
    Purge {
        /// Remove the entire package cache, not just unused packages.
        #[arg(short, long)]
        all: bool,
    },
    Completions {
        /// The shell to generate the completions for.
        #[arg(value_enum)]
        shell: clap_complete_command::Shell,
    },
}
