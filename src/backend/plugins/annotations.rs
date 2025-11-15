use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
struct FunctionAnnotation {
    name: String,
    args: Vec<(String, Annotation)>,
    // return_type: Annotation,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(untagged)]
enum Annotation {
    SimpleType { type_name: String },
    Union { type_name: String, args: Vec<Annotation> },
    List { type_name: String, args: Vec<Annotation> },
    Dict { type_name: String, args: Vec<Annotation>, values: Vec<Annotation> },
}

#[pyfunction]
fn load_annotations() -> PyResult<Vec<FunctionAnnotation>> {
    let json_data = fs::read_to_string("annotations.json")?;
    let annotations: Vec<FunctionAnnotation> = serde_json::from_str(&json_data)?;
    Ok(annotations)
}
