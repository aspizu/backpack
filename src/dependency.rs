use std::fmt::Display;

use arcstr::ArcStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Dependency {
    pub name: ArcStr,
    pub url: ArcStr,
    pub version: Option<ArcStr>,
}

impl Dependency {
    pub fn new(name: ArcStr, spec: ArcStr) -> Self {
        let (url, version) = spec
            .split_once('@')
            .map(|(url, version)| (url.into(), Some(version.into())))
            .unwrap_or_else(|| (spec, None));
        if url.starts_with("git@")
            || url.starts_with("http://")
            || url.starts_with("https://")
            || url.starts_with("file://")
            || url.starts_with("/")
            || url.starts_with("./")
            || url.starts_with("../")
        {
            Self { name, url, version }
        } else if url.starts_with("github.com/") {
            Self {
                name,
                url: ArcStr::from(format!("https://{}", url)),
                version,
            }
        } else {
            Self {
                name,
                url: ArcStr::from(format!("https://github.com/{}", url)),
                version,
            }
        }
    }
}

impl Display for Dependency {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.url)?;
        if let Some(version) = &self.version {
            write!(f, "@{}", version)?;
        }
        Ok(())
    }
}
