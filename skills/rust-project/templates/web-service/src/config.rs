use config::{Config, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct AppConfig {
    pub listen_addr: String,
    pub database_url: String,
    pub log_level: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            listen_addr: "127.0.0.1:3000".into(),
            database_url: "postgres://localhost/myapp".into(),
            log_level: "debug".into(),
        }
    }
}

pub fn load() -> anyhow::Result<AppConfig> {
    let config = Config::builder()
        // Start with defaults
        .set_default("listen_addr", "127.0.0.1:3000")?
        .set_default("log_level", "debug")?
        // Load from config file if exists
        .add_source(File::with_name("config/default").required(false))
        .add_source(File::with_name("config/local").required(false))
        // Override with environment variables (APP_ prefix)
        .add_source(
            Environment::with_prefix("APP")
                .separator("__")
                .try_parsing(true),
        )
        .build()?;

    Ok(config.try_deserialize()?)
}
