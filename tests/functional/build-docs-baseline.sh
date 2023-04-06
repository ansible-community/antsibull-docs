#!/bin/bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e


make_docsite_baseline() {
    DEST="$1"
    shift

    echo "Building baseline ${DEST}..."
    rm -rf "${DEST}"
    mkdir -p "${DEST}"
    ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --dest-dir "${DEST}" --use-current "$@" 2>&1 | (
        set +e
        grep -v "ERROR:antsibull:func=create_plugin_rst:mod=antsibull_docs.write_docs.plugins:nonfatal_errors="
        set -e
    )

    rstcheck --report-level warning --ignore-roles ansible-option-default,ansible-rv-sample-value,ansopt,ansval,ansretval -r "${DEST}" 2>&1 | (
        set +e
        grep -v "CRITICAL:rstcheck_core.checker:An \`AttributeError\` error occured."
        set -e
    )
}


make_ansible_doc_extract() {
    DEST="$1"
    shift

    echo "Build ansible-doc --metadata-dump --no-fail-on-errors $@ output cache"
    ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ ansible-doc --metadata-dump --no-fail-on-errors "$@" | python sanitize-ansible-doc-dump.py > "${DEST}.json"
}


make_docsite_baseline baseline-default ns.col1 ns.col2 ns2.col
make_docsite_baseline baseline-no-breadcrumbs ns.col1 ns.col2 ns2.col --no-breadcrumbs
make_docsite_baseline baseline-no-indexes ns.col1 ns2.col --fail-on-error --no-indexes
make_docsite_baseline baseline-use-html-blobs ns2.col --fail-on-error --use-html-blobs
make_docsite_baseline baseline-squash-hierarchy ns2.col --fail-on-error --squash-hierarchy

make_ansible_doc_extract ansible-doc-cache-all
make_ansible_doc_extract ansible-doc-cache-ns.col1 ns.col1
make_ansible_doc_extract ansible-doc-cache-ns.col2 ns.col2
make_ansible_doc_extract ansible-doc-cache-ns2.col ns2.col
