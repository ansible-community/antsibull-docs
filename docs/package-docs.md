<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# The official Ansible docsite

antsibull-docs is used in the build pipeline of the official Ansible docsites at [docs.ansible.com/ansible/devel](https://docs.ansible.com/ansible/devel/) and [docs.ansible.com/ansible/latest](https://docs.ansible.com/ansible/latest/) to generate the documentation for all collections included in Ansible. It is also used for the [ansible-core documentation](https://docs.ansible.com/ansible-core/devel/) to generate the documentation for `ansible.builtin`, the collection included with ansible-core.

The RST sources for all other files of the Ansible docsite can be found in the [ansible/ansible-documentation GitHub repository](https://github.com/ansible/ansible-documentation/). This repository also contains the docsite build scripts. antsibull-docs is called from [hacking/build_library/build_ansible/command_plugins/docs_build.py](https://github.com/ansible/ansible-documentation/blob/devel/hacking/build_library/build_ansible/command_plugins/docs_build.py). This uses the `devel` and `stable` subcommands of antsibull-docs. For its input, data from the [ansible-community/ansible-build-data GitHub repository](https://github.com/ansible-community/ansible-build-data) is used. For building stable docs for a major Ansible version `$X`, the latest `ansible-$X.$Y.$Z.deps` file in the `$X/` directory in `ansible-build-data` is used. For building the `devel` docs, the list of collections is used from the latest `$Y/ansible.in` file in `ansible-build-data` with the largest `$Y` that can be found in the repository. Then the latest version of every collection listed in `$Y/ansible.in` is used.

For the exact build process, please refer to the build process in the ansible-documentation repository.
