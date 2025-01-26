use arcstr::ArcStr;
use fxhash::FxHashMap;
use serde::Deserialize;
use serde::Serialize;

#[derive(Default, Serialize, Deserialize)]
pub struct Manifest {
    #[serde(default)]
    pub dependencies: FxHashMap<ArcStr, ArcStr>,
}
