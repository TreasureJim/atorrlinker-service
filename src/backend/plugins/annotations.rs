use pyo3::{prelude::*};

#[pyclass]
#[derive(Debug, Clone)]
enum PrimitiveType {
    Int,
    Float,
    Str,
    Bool,
}

#[pyclass]
#[derive(Debug, Clone)]
enum TypeInfo {
    Union(Vec<TypeInfo>),
    List(Vec<TypeInfo>),
    Dict(Vec<TypeInfo>, Vec<TypeInfo>),
    Primitive(PrimitiveType),
    Unknown(String),
}

#[pyclass]
#[derive(Debug, Clone)]
struct FunctionInfo {
    name: String,
    args: Vec<(String, TypeInfo)>,
    return_type: TypeInfo,
}
