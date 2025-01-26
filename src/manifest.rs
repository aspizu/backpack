use arcstr::ArcStr;
use fxhash::FxHashMap;
use serde::Deserialize;
use serde::Serialize;

#[derive(Default, Serialize, Deserialize)]
#[serde(default)]
pub struct Manifest {
    pub dependencies: FxHashMap<ArcStr, ArcStr>,
}
