mod annotations;

use std::{
    fs, io,
    path::{Path, PathBuf},
};

const PLUGIN_INFO_FUNC_NAME: &'static str = "atorrlinker_advertise";

use pyo3::{prelude::*, types::*};
use thiserror::Error;

use crate::config::Config;

// Adds the path to pythons sys path list
fn python_add_path(path: impl AsRef<Path>) {
    pyo3::Python::attach(|py| {
        let syspath = py
            .import("sys")
            .unwrap()
            .getattr("path")
            .unwrap()
            .cast_into::<pyo3::types::PyList>()
            .unwrap();
        syspath.insert(0, path.as_ref()).unwrap();
    });
}

#[derive(Error, Debug)]
pub enum PluginError {
    #[error("Failed to read directory: {0}")]
    IoError(#[from] io::Error),

    #[error("Failed to get file name: {0}")]
    FileNameError(String),

    #[error("Failed to convert file name to string: {0}")]
    ToStrError(String),
}

pub struct Plugin {
    name: String,
    module: PyModule,
    arguments: Vec<FuncInfo>,
}

impl Plugin {
    /// Requires full path to main python file
    pub fn from_path(path: impl AsRef<Path>) -> Self {
        // https://pyo3.rs/v0.27.1/python-from-rust/calling-existing-code.html
        // Add module to pythons path 
        python_add_path(&path);

        Plugin::get_plugin_functions(&path);
    }

    pub fn name_to_path(base_path: impl AsRef<Path>, name: &str) -> PathBuf {
        base_path.as_ref().join(name).join("main.py")
    }

    pub fn get_plugin_functions(path: impl AsRef<Path>) -> Vec<String> {
        todo!("Call advertising function");
        todo!("Parse annotations");
    }

    pub fn plugin_name_from_path(plugin_root: impl AsRef<Path>, name: String) -> PathBuf {
        plugin_root.as_ref().join(name)
    }
}

pub enum FunctionArgumentType {
    String,
    Number,
    List(Box<FunctionArgumentType>),
}

pub struct FuncInfo {
    name: String,
    arguments: Vec<(String, FunctionArgumentType)>,
}

pub fn list_plugins(folder: impl AsRef<Path>) -> Result<Vec<(String, PathBuf)>, PluginError> {
    let mut plugin_paths = Vec::new();

    for f in fs::read_dir(folder)?.into_iter() {
        let path = f?.path();
        if !path.is_dir() {
            continue;
        }

        let path = (
            path.as_path()
                .file_name()
                .ok_or_else(|| PluginError::FileNameError(path.to_string_lossy().to_string()))?
                .to_str()
                .ok_or_else(|| PluginError::ToStrError(path.to_string_lossy().to_string()))?
                .to_string(),
            path,
        );
        plugin_paths.push(path);
    }
    Ok(plugin_paths)
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::*;
    use pyo3::{prelude::*, types::*};
}
