#!/bin/bash
set -e
MYPYPATH=stubs/ poetry run mypy src/antsibull_docs src/sphinx_antsibull_ext "$@"
