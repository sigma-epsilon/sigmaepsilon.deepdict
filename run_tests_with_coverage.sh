#!/bin/bash

# Set default rc_path
rc_path=".coveragerc"

# Set the COVERAGE_RCFILE to the chosen rc_path
export COVERAGE_RCFILE=$rc_path

# Run the coverage commands using the specified .coveragerc file
uv run coverage run --source=src -m pytest
uv run coverage xml
uv run coverage html

