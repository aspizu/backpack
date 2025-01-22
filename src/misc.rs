use std::time::SystemTime;
use std::time::UNIX_EPOCH;

use arcstr::ArcStr;
use rand::distributions::Alphanumeric;
use rand::distributions::DistString;

pub fn generate_random_id() -> ArcStr {
    Alphanumeric
        .sample_string(&mut rand::thread_rng(), 8)
        .into()
}

pub fn seconds_since_epoch() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}
