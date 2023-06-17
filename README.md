# `commons` 📦

## Description

`commons` is a Python 3 library containing useful implementations for all CRS modules:

- Utility functions and classes;
- Interfaces; and
- Enumerations.

The enumerations are not exhaustive. They define the minimal set of members that are used in OpenCRS. For example, `InputStreams` doesn't define an `ENVIRONMENT_VARIABLE` (a valid input stream for an executable) as this case is not tacked yet by the project.

## Setup

Install the required Python 3 packages via `poetry install --no-dev`.

## Usage

1. Install the required Python 3 packages via `poetry install --no-dev`.
2. If the `ghidra` or `qbdi` modules will be used, ensure you have Docker installed.
3. If the `ghidra` will be used, build the Docker image: `docker build --tag ghidra -f commons/ghidra/docker/Dockerfile commons/ghidra/docker`
4. If the `qbdi` will be used, build the Docker image: `docker build --tag qbdi_args_fuzzing -f commons/qbdi/Dockerfile.qbdi_docker commons/qbdi`
