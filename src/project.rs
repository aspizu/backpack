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
        for dependency in &package.dependencies {
            let dependency = dependency.clone();
            let packages_cache = self.packages_cache.clone();
            let backpack = self.backpack.clone();
            handles.push(thread::spawn(move || {
                let path = packages_cache
                    .lock()
                    .unwrap()
                    .get_package(&dependency)
                    .unwrap();
                backpack
                    .lock()
                    .unwrap()
                    .add_package(dependency.name, &path)
                    .unwrap();
            }));
        }
        for handle in handles {
            handle.join().unwrap();
        }
        for dependency in &package.dependencies {
            let packages_cache = self.packages_cache.clone();
            let path = packages_cache.lock().unwrap().get_package(dependency)?;
            let dependency = Package::new(path)?;
            self.add_dependencies_for_package(&dependency)?;
        }
        Ok(())
    }
}
