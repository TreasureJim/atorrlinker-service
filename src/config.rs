use std::path::PathBuf;

use once_cell::sync::OnceCell;

static CONFIG: OnceCell<Config> = OnceCell::new();

macro_rules! get_env_var {
    ($name:expr) => {{
        std::env::var($name).expect(&format!("Could not find {} environment variable.", $name))
    }};
}

pub struct Config {
    pub api_base: String,
    pub plugin_path: PathBuf,
}

impl Config {
    pub fn new() -> &'static Self {
        CONFIG.get_or_init(|| Self {
            api_base: get_env_var!("API_BASE"),
            plugin_path: get_env_var!("PLUGIN_BASE_PATH").into(),
        })
    }
}
