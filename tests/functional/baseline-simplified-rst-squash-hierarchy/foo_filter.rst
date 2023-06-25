

ns2.col.foo filter -- The foo filter \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. note::
    This filter plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 1.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Do some fooing.







Input
-----

This describes the input of the filter, the value before ``| ns2.col.foo``.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-_input:

      **Input**

      :literal:`string` / :strong:`required`




      .. raw:: html

        </div></div>

    - 
      The main input.






Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ns2.col.foo(key1=value1, key2=value2, ...)``

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-bar:

      **bar**

      :literal:`string`




      .. raw:: html

        </div></div>

    - 
      Some bar.



  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-foo:

      **foo**

      :literal:`list` / :literal:`elements=dictionary` / :strong:`required`




      .. raw:: html

        </div></div>

    - 
      Some foo.







Examples
--------

.. code-block:: yaml+jinja

    
    some_var: "{{ 'foo' | ns2.col.foo }}"





Return Value
------------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _return-_value:

      **Return value**

      :literal:`string`

      .. raw:: html

        </div></div>
    - 
      The result.


      Returned: success





.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

