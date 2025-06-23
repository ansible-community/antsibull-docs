..
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.ns2.col.docsite.filter_guide:

Filter Guide
============

.. contents:: Contents
   :local:
   :depth: 1

The :anscollection:`ns2.col collection <ns2.col>` offers :anscollection:`two filters <ns2.col#plugins-filter>`.

- :ansplugin:`ns2.col.foo#filter`: foo! (Note its :ansopt:`ns2.col.foo#filter:foo[]` option, and try :ansopt:`ns2.col.foo#filter:bar=baz`.)
- :ansplugin:`ns2.col.bar#filter`: bar! (Its return value is :ansretval:`ns2.col.bar#filter:_value`.)

.. envvar:: FOOBAR1

    This is one environment variable.

.. envvar:: FOOBAR2

    This is another environment variable.

.. envvar:: FOOBAR3

    This is a third environment variable.

.. note::
  Also check out the :ansplugin:`ns2.col.foo role <ns2.col.foo#role>` with its :ansplugin:`main <ns2.col.foo#role:main>` entrypoint.

Errors
------

:anscollection:`does.not_exist`

:anscollection:`ns2.col#foobar`

:anscollection:`ns.col1#plugins-filter`

:anscollection:`ns2.col#plugins-foo`

:ansplugin:`ns2.col.does_not_exist#filter`

:ansplugin:`ns2.col.foo#asdf`

:ansplugin:`ns2.col.foo#filter:boo`

:ansplugin:`ns2.col.foo#role:boo`

:ansopt:`ns2.col.foo#role:main:does_not_exist`

:ansopt:`ns2.col.foo#role:does_not_exist:neither`

:ansopt:`ns2.col.foo#role:does_not_exist`
