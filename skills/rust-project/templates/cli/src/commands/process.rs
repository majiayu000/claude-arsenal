use anyhow::{Context, Result};
use std::path::Path;
use tracing::{info, warn};

use super::OutputFormat;

pub fn run(files: &[std::path::PathBuf], output: &Path, format: &OutputFormat) -> Result<()> {
    info!("Processing {} files", files.len());

    // Create output directory if it doesn't exist
    std::fs::create_dir_all(output)
        .with_context(|| format!("failed to create output directory: {}", output.display()))?;

    for file in files {
        if !file.exists() {
            warn!("File not found: {}", file.display());
            continue;
        }

        info!("Processing: {}", file.display());
        process_file(file, output, format)?;
    }

    info!("Done!");
    Ok(())
}

fn process_file(input: &Path, output: &Path, format: &OutputFormat) -> Result<()> {
    let content = std::fs::read_to_string(input)
        .with_context(|| format!("failed to read: {}", input.display()))?;

    let output_name = input
        .file_stem()
        .map(|s| s.to_string_lossy().to_string())
        .unwrap_or_else(|| "output".into());

    let extension = match format {
        OutputFormat::Json => "json",
        OutputFormat::Yaml => "yaml",
        OutputFormat::Text => "txt",
    };

    let output_path = output.join(format!("{}.{}", output_name, extension));

    // Process content (placeholder)
    let processed = content.to_uppercase();

    std::fs::write(&output_path, processed)
        .with_context(|| format!("failed to write: {}", output_path.display()))?;

    info!("Wrote: {}", output_path.display());
    Ok(())
}
