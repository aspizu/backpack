use std::path::PathBuf;

use anyhow::Context;

use crate::manifest::Manifest;

pub struct Package {
    pub path: PathBuf,
    pub manifest: Manifest,
}

impl Package {
    pub fn new(path: PathBuf) -> anyhow::Result<Self> {
        let manifest = if let Ok(text) = std::fs::read_to_string(path.join("goboscript.toml")) {
            toml::from_str(&text).context("Failed to parse goboscript.toml")?
        } else {
            Manifest::default()
        };
        Ok(Self { path, manifest })
    }
}
