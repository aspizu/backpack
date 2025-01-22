use std::path::PathBuf;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

use crate::backpack::Backpack;
use crate::package::Package;
use crate::packages_cache::PackagesCache;

pub struct Project {
    package: Package,
    packages_cache: Arc<Mutex<PackagesCache>>,
    backpack: Arc<Mutex<Backpack>>,
}

impl Project {
    pub fn new(path: PathBuf, packages_cache: Arc<Mutex<PackagesCache>>) -> anyhow::Result<Self> {
        Ok(Self {
            backpack: Arc::new(Mutex::new(Backpack::new(path.join("backpack"))?)),
            package: Package::new(path)?,
            packages_cache,
        })
    }

    fn add_dependencies_for_package(&self, package: &Package) -> anyhow::Result<()> {
        let mut handles = vec![];
        for (name, url) in &package.manifest.dependencies {
            let name = name.clone();
            let url = url.clone();
            let packages_cache = self.packages_cache.clone();
            let backpack = self.backpack.clone();
            handles.push(thread::spawn(move || {
                let path = packages_cache.lock().unwrap().get_package(url).unwrap();
                backpack.lock().unwrap().add_package(name, &path).unwrap();
            }));
        }
        for handle in handles {
            handle.join().unwrap();
        }
        for (name, url) in &package.manifest.dependencies {
            let packages_cache = self.packages_cache.clone();
            let backpack = self.backpack.clone();
            let path = packages_cache.lock().unwrap().get_package(url.clone())?;
            let dependency = Package::new(path)?;
            if !backpack.lock().unwrap().contains_package(name) {
                self.add_dependencies_for_package(&dependency)?;
            }
        }
        Ok(())
    }

    pub fn sync(&self) -> anyhow::Result<()> {
        self.add_dependencies_for_package(&self.package)
    }
}
