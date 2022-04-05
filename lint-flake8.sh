#!/bin/bash
set -e
poetry run flake8 src/antsibull_docs src/sphinx_antsibull_ext --count --max-complexity=10 --max-line-length=100 --statistics "$@"
