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
    NAME="$1"
    shift

    echo "Build ansible-galaxy collection list $@ output cache"
    ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ ansible-galaxy collection list --format json "$@" | python sanitize-ansible-galaxy-list.py > "ansible-galaxy-cache-${NAME}.json"

    echo "Build ansible-doc --metadata-dump --no-fail-on-errors $@ output cache"
    ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ ansible-doc --metadata-dump --no-fail-on-errors "$@" | python sanitize-ansible-doc-dump.py > "ansible-doc-cache-${NAME}.json"
}


make_docsite_baseline baseline-default ns.col1 ns.col2 ns2.col ns2.flatcol
make_docsite_baseline baseline-no-breadcrumbs ns.col1 ns.col2 ns2.col ns2.flatcol --no-breadcrumbs
make_docsite_baseline baseline-no-indexes ns.col1 ns2.col ns2.flatcol --fail-on-error --no-indexes
make_docsite_baseline baseline-use-html-blobs ns2.col --fail-on-error --use-html-blobs
make_docsite_baseline baseline-squash-hierarchy ns2.col --fail-on-error --squash-hierarchy

echo "Build ansible --version output cache"
ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ ansible --version | sed -e "s|${PWD}/collections|<<<<<COLLECTIONS>>>>>|g" | sed -e "s|${HOME}|<<<<<HOME>>>>>|g" | sed -E "s|(ansible python module location = ).*|\\1<<<<<ANSIBLE>>>>>|g" > ansible-version.output

make_ansible_doc_extract all
make_ansible_doc_extract ns.col1 ns.col1
make_ansible_doc_extract ns.col2 ns.col2
make_ansible_doc_extract ns2.col ns2.col
make_ansible_doc_extract ns2.flatcol ns2.flatcol
