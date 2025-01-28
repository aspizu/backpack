use std::path::PathBuf;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

use fxhash::FxHashSet;

use crate::backpack::Backpack;
use crate::package::Package;
use crate::packages_cache::PackagesCache;

pub struct Project {
    packages_cache: Arc<Mutex<PackagesCache>>,
    backpack: Arc<Mutex<Backpack>>,
    synced: FxHashSet<PathBuf>,
}

impl Project {
    pub fn new(path: PathBuf, packages_cache: Arc<Mutex<PackagesCache>>) -> anyhow::Result<Self> {
        Ok(Self {
            backpack: Arc::new(Mutex::new(Backpack::new(path.join("backpack"))?)),
            packages_cache,
            synced: Default::default(),
        })
    }

    pub fn add_dependencies_for_package(&mut self, package: &Package) -> anyhow::Result<()> {
        if self.synced.contains(&package.path) {
            return Ok(());
        }
        self.synced.insert(package.path.clone());
        let mut handles = vec![];
        println!(
            "adding dependencies from package {}",
            package.path.display()
        );
        for (name, url) in &package.manifest.dependencies {
            let name = name.clone();
            let url = url.clone();
            let packages_cache = self.packages_cache.clone();
            let backpack = self.backpack.clone();
            println!("adding dependency {}", url);
            handles.push(thread::spawn(move || {
                let path = packages_cache.lock().unwrap().get_package(url).unwrap();
                backpack.lock().unwrap().add_package(name, &path).unwrap();
            }));
        }
        for handle in handles {
            handle.join().unwrap();
        }
        for url in package.manifest.dependencies.values() {
            let packages_cache = self.packages_cache.clone();
            let path = packages_cache.lock().unwrap().get_package(url.clone())?;
            let dependency = Package::new(path)?;
            self.add_dependencies_for_package(&dependency)?;
        }
        Ok(())
    }
}
