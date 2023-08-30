#!/bin/bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e


make_baseline() {
    DEST="$1"
    shift

    echo "Building baseline ${DEST}..."
    rm -rf "${DEST}"
    mkdir -p "${DEST}"
    python antsibull-docs-stub.py sphinx-init --dest-dir "${DEST}" "$@" > /dev/null
    sed -i -e 's/^cd .*$/cd DESTINATION/g' "${DEST}/build.sh"
}


make_baseline baseline-sphinx-init-current --use-current
make_baseline baseline-sphinx-init-collections ns.col1 ns.col2 ns2.col
make_baseline baseline-sphinx-init-config ns.col1 --no-indexes --no-breadcrumbs --use-html-blobs --squash-hierarchy --lenient --fail-on-error \
    --index-rst-source test.rst \
    --intersphinx identifier:https://server/path --intersphinx foo:https://bar/baz \
    --sphinx-theme another-theme
make_baseline baseline-sphinx-init-extra ns.col1 \
    --extra-conf key=value --extra-conf "long key=very \"long\" 'value'" \
    --extra-html-context key=value --extra-html-context "long key=very \"long\" 'value'" \
    --extra-html-theme-options key=value --extra-html-theme-options "long key=very \"long\" 'value'" \
    --project "Foo 'bar'" --copyright "Baz \"bam'" --title "A title" --html-short-title "A shorter title - not"
