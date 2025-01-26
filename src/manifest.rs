use arcstr::ArcStr;
use fxhash::FxHashMap;
use serde::Deserialize;
use serde::Serialize;

#[derive(Default, Serialize, Deserialize)]
pub struct Manifest {
    pub dependencies: FxHashMap<ArcStr, ArcStr>,
}

impl From<PartialManifest> for Manifest {
    fn from(partial: PartialManifest) -> Self {
        Self {
            dependencies: partial.dependencies.unwrap_or_default(),
        }
    }
}

#[derive(Default, Serialize, Deserialize)]
pub struct PartialManifest {
    pub dependencies: Option<FxHashMap<ArcStr, ArcStr>>,
}
