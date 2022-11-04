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
    ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --dest-dir "${DEST}" --use-current $@ 2>&1 | (
        set +e
        grep -v "An error page will be generated."
        set -e
    )

    rstcheck --report-level warning --ignore-roles ansible-option-default,ansible-rv-sample-value -r "${DEST}" 2>&1 | (
        set +e
        grep -v "CRITICAL:rstcheck_core.checker:An \`AttributeError\` error occured."
        set -e
    )
}


make_baseline baseline-default ns.col1 ns.col2 ns2.col
make_baseline baseline-no-breadcrumbs ns.col1 ns.col2 ns2.col --no-breadcrumbs
make_baseline baseline-no-indexes ns.col1 ns2.col --fail-on-error --no-indexes
make_baseline baseline-use-html-blobs ns2.col --fail-on-error --use-html-blobs
make_baseline baseline-squash-hierarchy ns2.col --fail-on-error --squash-hierarchy
