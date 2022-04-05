#!/bin/bash
set -e
poetry run pylint --rcfile .pylintrc.automated src/antsibull_docs src/sphinx_antsibull_ext "$@"
