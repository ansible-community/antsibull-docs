.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: <ANTSIBULL_DOCS_VERSION>

.. Anchors

.. _ansible_collections.ns.col2.foo2_module:

.. Anchors: short name for ansible.builtin

.. Title

ns.col2.foo2 module -- Foo two
++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install ns.col2`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.ns.col2.foo2_module_requirements>` for details.

    To use it in a playbook, specify: :code:`ns.col2.foo2`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Does some foo on the remote host.
- A broken reference :ref:`asdfasdfoobarTHISDOESNOTEXIST <asdfasdfoobarTHISDOESNOTEXIST>`.
- The option :ansopt:`ns.col2.foo2#module:foo` exists, but :ansopt:`ns.col2.foo2#module:foobar` does not.
- The return value :ansretval:`ns.col2.foo2#module:bar` exists, but :ansretval:`ns.col2.foo2#module:barbaz` does not.
- Again existing: :ansopt:`ns.col2.foo#module:foo=1`\ , :ansretval:`ns.col2.foo#module:bar=2`
- Again not existing: :ansopt:`ns.col2.foo#module:foobar=1`\ , :ansretval:`ns.col2.foo#module:barbaz=2`
- :literal:`\ ` :emphasis:`\ ` :strong:`\ ` :literal:`\ `   :ref:`\  <>` :ansval:`\ ` :ansopt:`ns.col2.foo2#module:`\  :ansretval:`ns.col2.foo2#module:`\  :ansenvvar:`\ `
- Foo bar baz. Bamm - Bar baz
  bam bum.
  Bumm - Foo bar
  baz bam!


.. Aliases


.. Requirements

.. _ansible_collections.ns.col2.foo2_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- Foo.






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-bar"></div>

      .. _ansible_collections.ns.col2.foo2_module__parameter-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-bar" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Bar.

      Some :ansopt:`ns.col2.foo2#module:broken markup`.

      Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-foo"></div>

      .. _ansible_collections.ns.col2.foo2_module__parameter-foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-foo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The foo source.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo"></div>

      .. _ansible_collections.ns.col2.foo2_module__parameter-subfoo:

      .. rst-class:: ansible-option-title

      **subfoo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some recursive foo.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo/BaZ"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns.col2.foo2_module__parameter-subfoo/baz:

      .. rst-class:: ansible-option-title

      **BaZ**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo/BaZ" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Funky.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.ns.col2.foo2_module__parameter-subfoo/foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A sub foo.

      Whatever.

      Also required when :emphasis:`subfoo` is specified when :emphasis:`foo=bar` or :literal:`baz`.

      :ansretval:`ns.col2.foo2#module:foobarbaz` does not exist.


      .. raw:: html

        </div>



.. Attributes


Attributes
----------

.. tabularcolumns:: \X{2}{10}\X{3}{10}\X{5}{10}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Attribute
    - Support
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-check_mode"></div>

      .. _ansible_collections.ns.col2.foo2_module__attribute-check_mode:

      .. rst-class:: ansible-option-title

      **check_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-check_mode" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Can run in check\_mode and return changed status prediction without modifying target


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-diff_mode"></div>

      .. _ansible_collections.ns.col2.foo2_module__attribute-diff_mode:

      .. rst-class:: ansible-option-title

      **diff_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-diff_mode" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-label:`Support: \ `\ :ansible-attribute-support-full:`full`


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode

      Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="attribute-platform"></div>

      .. _ansible_collections.ns.col2.foo2_module__attribute-platform:

      .. rst-class:: ansible-option-title

      **platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#attribute-platform" title="Permalink to this attribute"></a>

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      :ansible-attribute-support-property:`Platform:` |antsibull-internal-nbsp|:ansible-attribute-support-full:`posix`

      The module :strong:`ERROR while parsing`\ : While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN is not using an FQCN.

      Sometimes our markup is :strong:`ERROR while parsing`\ : While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter

      Foo bar baz. Bamm - Bar baz
      bam bum.
      Bumm - Foo bar
      baz bam!


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target OS/families that can be operated against


      .. raw:: html

        </div>



.. Notes

Notes
-----

.. note::
   - Foo bar baz. Bamm - Bar baz
     bam bum.
     Bumm - Foo bar
     baz bam!

.. Seealso

See Also
--------

.. seealso::

   :ref:`ns.col2.foo3 <ansible_collections.ns.col2.foo3_module>`
       Foo III.
   :ref:`ns.col2.foobarbaz <ansible_collections.ns.col2.foobarbaz_module>`
       The official documentation on the **ns.col2.foobarbaz** module.
   :ref:`ns.col2.foo4 <ansible_collections.ns.col2.foo4_module>` module plugin
       Markup reference linting test.
   :ref:`ns.col2.foobarbaz <ansible_collections.ns.col2.foobarbaz_inventory>` inventory plugin
       The official documentation on the **ns.col2.foobarbaz** inventory plugin.
   :ref:`ansible.builtin.service <ansible_collections.ansible.builtin.service_module>`
       The service module.
   :ref:`ansible.builtin.foobarbaz <ansible_collections.ansible.builtin.foobarbaz_module>`
       A non-existing module.
   :ref:`ansible.builtin.linear <ansible_collections.ansible.builtin.linear_strategy>` strategy plugin
       The linear strategy plugin.
   :ref:`ansible.builtin.foobarbaz <ansible_collections.ansible.builtin.foobarbaz_strategy>` strategy plugin
       Foo bar baz. Bamm - Bar baz
       bam bum.
       Bumm - Foo bar
       baz bam!

.. Examples

Examples
--------

.. code-block:: yaml+jinja

    name: This is YAML.



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-bar"></div>

      .. _ansible_collections.ns.col2.foo2_module__return-bar:

      .. rst-class:: ansible-option-title

      **bar**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-bar" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Some bar.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` success

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"baz"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Someone else (@ansible)



.. Extra links


.. Parsing errors
