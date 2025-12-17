mod process;

use anyhow::Result;
use clap::Subcommand;
use std::path::Path;

#[derive(Subcommand)]
pub enum Commands {
    /// Process input files
    Process {
        /// Input files to process
        #[arg(required = true)]
        files: Vec<std::path::PathBuf>,

        /// Output directory
        #[arg(short, long, default_value = "output")]
        output: std::path::PathBuf,

        /// Output format
        #[arg(short, long, default_value = "json")]
        format: OutputFormat,
    },

    /// Show configuration
    Config,

    /// Initialize a new project
    Init {
        /// Project name
        #[arg(default_value = ".")]
        path: std::path::PathBuf,
    },
}

#[derive(Clone, clap::ValueEnum)]
pub enum OutputFormat {
    Json,
    Yaml,
    Text,
}

impl Commands {
    pub fn execute(&self, config_path: &Path) -> Result<()> {
        match self {
            Commands::Process { files, output, format } => {
                process::run(files, output, format)
            }
            Commands::Config => {
                println!("Config path: {}", config_path.display());
                Ok(())
            }
            Commands::Init { path } => {
                println!("Initializing project at: {}", path.display());
                Ok(())
            }
        }
    }
}
