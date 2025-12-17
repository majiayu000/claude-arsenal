use anyhow::Result;
use clap::Parser;
use std::path::PathBuf;

mod commands;
mod error;

use commands::Commands;

#[derive(Parser)]
#[command(name = "mycli")]
#[command(version, about = "A CLI tool", long_about = None)]
struct Cli {
    /// Verbose output
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,

    /// Config file path
    #[arg(short, long, default_value = "config.toml")]
    config: PathBuf,

    #[command(subcommand)]
    command: Commands,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    // Initialize tracing based on verbosity
    let filter = match cli.verbose {
        0 => "warn",
        1 => "info",
        2 => "debug",
        _ => "trace",
    };

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .init();

    // Execute command
    cli.command.execute(&cli.config)?;

    Ok(())
}
