use arcstr::ArcStr;
use fxhash::FxHashMap;
use serde::Deserialize;
use serde::Serialize;

#[derive(Default, Serialize, Deserialize)]
pub struct Manifest {
    pub dependencies: FxHashMap<ArcStr, ArcStr>,
}
