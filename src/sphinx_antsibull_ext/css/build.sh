#!/bin/bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

SASS=${SASS_COMPILER:-node_modules/.bin/sass}
POSTCSS=${POSTCSS:-node_modules/.bin/postcss}

if [ ! -x "${SASS}" ]; then
    echo "${SASS} is not executable. Did you run 'npm install'?"
    exit -1
fi

if [ ! -x "${POSTCSS}" ]; then
    echo "${POSTCSS} is not executable. Did you run 'npm install'?"
    exit -1
fi

export BROWSERSLIST_CONFIG=browserslistrc

# Apparently the cssnano.config.js needs to be where the destination file is placed
trap "{ rm -f ../cssnano.config.js; }" EXIT
cp cssnano.config.js ..

set -e

build_css() {
    SOURCE="$1.scss"
    DEST="../$1.css"
    set -x
    ${SASS} --no-source-map "${SOURCE}" "${DEST}"
    ${POSTCSS} --use autoprefixer --use cssnano --no-map -r "${DEST}"
    { set +x; } 2>/dev/null  # https://stackoverflow.com/a/19226038
}

build_css antsibull-minimal
build_css colors-default
build_css colors-default-autodark
build_css colors-default-dark

grep -Fq '/* INSERT COLOR SCHEME HERE */' ../antsibull-minimal.css || (echo -e "\nERROR: Placeholder not found!" ; exit 1)
