use std::path::PathBuf;

use anyhow::Context;

use crate::manifest::Manifest;

pub struct Package {
    pub path: PathBuf,
    pub manifest: Manifest,
}

impl Package {
    pub fn new(path: PathBuf) -> anyhow::Result<Self> {
        let goboscript_toml_path = path.join("goboscript.toml");
        let manifest = if let Ok(text) = std::fs::read_to_string(&goboscript_toml_path) {
            toml::from_str(&text)
                .with_context(|| format!("Failed to parse {}", goboscript_toml_path.display()))?
        } else {
            Manifest::default()
        };
        Ok(Self { path, manifest })
    }
}
