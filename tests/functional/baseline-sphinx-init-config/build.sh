#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

set -e

pushd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
trap "{ popd; }" EXIT

# Create collection documentation into temporary directory
rm -rf temp-rst
mkdir -p temp-rst
chmod og-w temp-rst  # antsibull-docs wants that directory only readable by itself
antsibull-docs \
    --config-file antsibull-docs.cfg \
    collection \
    --fail-on-error \
    --squash-hierarchy \
    --output-format ansible-docsite \
    --dest-dir temp-rst \
    ns.col1

# Copy collection documentation into source directory
rsync -cprv --delete-after temp-rst/ rst/

# Build Sphinx site
sphinx-build -M html rst build -c .

