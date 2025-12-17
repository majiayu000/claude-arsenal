use thiserror::Error;

#[derive(Debug, Error)]
pub enum CliError {
    #[error("file not found: {0}")]
    FileNotFound(String),

    #[error("invalid format: {0}")]
    InvalidFormat(String),

    #[error("io error: {0}")]
    Io(#[from] std::io::Error),

    #[error("parse error: {0}")]
    Parse(String),
}
