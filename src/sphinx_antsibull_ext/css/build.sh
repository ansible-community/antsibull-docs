#!/bin/bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

SASS=${SASS_COMPILER:-$(which sass)}
POSTCSS=${POSTCSS:-$(which postcss)}

if [ "${SASS}" == "" ]; then
    echo "Need 'sass' on path. You can install sass with 'npm install sass'."
    exit -1
fi

if [ "${POSTCSS}" == "" ]; then
    echo "Need 'postcss' on path. You can install postcss and the required plugins with 'npm install autoprefixer cssnano postcss postcss-cli'."
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
