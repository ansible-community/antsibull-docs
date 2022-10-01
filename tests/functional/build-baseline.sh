#!/bin/sh
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e
rm -rf baseline-default baseline-no-breadcrumbs baseline-no-indexes baseline-use-html-blobs baseline-squash-hierarchy
mkdir -p baseline-default baseline-no-breadcrumbs baseline-no-indexes baseline-use-html-blobs baseline-squash-hierarchy

ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --fail-on-error --use-current ns.col1 ns.col2 ns2.col --dest-dir baseline-default
ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --fail-on-error --use-current ns.col1 ns.col2 ns2.col --dest-dir baseline-no-breadcrumbs --no-breadcrumbs
ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --fail-on-error --use-current ns.col1 ns.col2 ns2.col --dest-dir baseline-no-indexes --no-indexes
ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --fail-on-error --use-current ns2.col --dest-dir baseline-use-html-blobs --use-html-blobs
ANSIBLE_COLLECTIONS_PATHS= ANSIBLE_COLLECTIONS_PATH=collections/ antsibull-docs collection --fail-on-error --use-current ns2.col --dest-dir baseline-squash-hierarchy --squash-hierarchy
