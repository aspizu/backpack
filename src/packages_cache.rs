use std::fs;
use std::fs::File;
use std::io::BufReader;
use std::io::BufWriter;
use std::path::PathBuf;
use std::process::Command;
use std::process::Stdio;

use anyhow::Context;
use arcstr::ArcStr;
use fxhash::FxHashMap;
use rmp_serde::Serializer;
use serde::Deserialize;
use serde::Serialize;

use crate::misc::generate_random_id;
use crate::misc::seconds_since_epoch;

#[derive(Serialize, Deserialize)]
struct PackagesCacheEntry {
    id: ArcStr,
    last_used: u64,
}

pub struct PackagesCache {
    path: PathBuf,
    index_path: PathBuf,
    index: FxHashMap<ArcStr, PackagesCacheEntry>,
}

impl PackagesCache {
    pub fn new(path: PathBuf) -> anyhow::Result<Self> {
        fs::create_dir_all(&*path).context("Failed to create package cache directory")?;
        let index_path = path.join("index.bin");
        let index = if let Ok(index_file) = File::open(&index_path) {
            let mut reader = BufReader::new(index_file);
            rmp_serde::from_read(&mut reader)
                .context("Failed to deserialize package cache index")?
        } else {
            FxHashMap::default()
        };
        Ok(Self {
            path,
            index_path,
            index,
        })
    }

    pub fn get_package(&mut self, url: ArcStr) -> anyhow::Result<PathBuf> {
        if let Some(entry) = self.index.get_mut(&url) {
            entry.last_used = seconds_since_epoch();
            Ok(self.path.join(&*entry.id))
        } else {
            let id = self.clone_package(url)?;
            Ok(self.path.join(&*id))
        }
    }

    pub fn purge(&mut self) -> anyhow::Result<()> {
        let mut error = Ok(());
        self.index.retain(|_, entry| {
            if let Err(err) = fs::remove_dir_all(self.path.join(&*entry.id)) {
                error = Err(err.into());
            }
            entry.last_used + 60 * 60 * 24 * 7 < seconds_since_epoch()
        });
        error
    }

    fn clone_package(&mut self, url: ArcStr) -> anyhow::Result<ArcStr> {
        let id = generate_random_id();
        let entry = PackagesCacheEntry {
            id: id.clone(),
            last_used: seconds_since_epoch(),
        };
        self.index.insert(url.clone(), entry);
        let (repo, version) = url.rsplit_once('@').unwrap_or_else(|| (&url, "main"));
        Command::new("git")
            .args([
                "clone",
                "--depth=1",
                "--branch",
                version,
                repo,
                self.path.join(&*id).to_str().unwrap(),
            ])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .with_context(|| format!("Failed to clone package {}", url))?;
        Ok(self.index[&url].id.clone())
    }
}

impl Drop for PackagesCache {
    fn drop(&mut self) {
        let Ok(mut file) = File::create(&self.index_path) else {
            return;
        };
        let mut writer = BufWriter::new(&mut file);
        let Ok(()) = self.index.serialize(&mut Serializer::new(&mut writer)) else {
            return;
        };
    }
}
