
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.ns.col2.foo2_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

ns.col2.foo2 module -- Foo two
++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ns/col2>`_ (version 0.0.1).

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
- A broken reference \ :ref:`asdfasdfoobarTHISDOESNOTEXIST <asdfasdfoobarTHISDOESNOTEXIST>`\ .
- The option \ :ansopt:`ns.col2.foo2#module:foo`\  exists, but \ :ansopt:`ns.col2.foo2#module:foobar`\  does not.
- The return value \ :ansretval:`ns.col2.foo2#module:bar`\  exists, but \ :ansretval:`ns.col2.foo2#module:barbaz`\  does not.
- Again existing: \ :ansopt:`ns.col2.foo#module:foo=1`\ , \ :ansretval:`ns.col2.foo#module:bar=2`\ 
- Again not existing: \ :ansopt:`ns.col2.foo#module:foobar=1`\ , \ :ansretval:`ns.col2.foo#module:barbaz=2`\ 


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

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

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

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Bar.

      Some \ :ansopt:`ns.col2.foo2#module:broken markup`\ .


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

      .. rst-class:: ansible-option-type-line

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

      .. rst-class:: ansible-option-type-line

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
        <div class="ansibleOptionAnchor" id="parameter-subfoo/foo"></div>

      .. _ansible_collections.ns.col2.foo2_module__parameter-subfoo/foo:

      .. rst-class:: ansible-option-title

      **foo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subfoo/foo" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A sub foo.

      Whatever.

      Also required when \ :emphasis:`subfoo`\  is specified when \ :emphasis:`foo=bar`\  or \ :literal:`baz`\ .

      \ :ansretval:`ns.col2.foo2#module:foobarbaz`\  does not exist.


      .. raw:: html

        </div>



.. Attributes


Attributes
----------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

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

      The module \ :strong:`ERROR while parsing`\ : While parsing "M(boo)" at index 12: Module name "boo" is not a FQCN\  is not using an FQCN.

      Sometimes our markup is \ :strong:`ERROR while parsing`\ : While parsing "B(broken." at index 25: Cannot find closing ")" after last parameter\ 


      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target OS/families that can be operated against


      .. raw:: html

        </div>



.. Notes


.. Seealso


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

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

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

      .. rst-class:: ansible-option-type-line

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

