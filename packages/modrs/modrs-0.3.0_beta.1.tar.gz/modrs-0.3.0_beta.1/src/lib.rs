use pyo3::prelude::*;
use std::env;
/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn _cli() -> PyResult<String> {
    let args: Vec<String> = env::args().collect();
    let mut cli="hello i am working";

    if args.len() > 2 {
        cli=&args[2];
    }
    Ok(cli.to_string())
}

#[pymodule]
fn modrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum, m)?)?;
    m.add_function(wrap_pyfunction!(_cli, m)?)?;
    Ok(())
}
