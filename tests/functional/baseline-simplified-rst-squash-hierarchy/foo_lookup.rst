

ns2.col.foo lookup -- Look up some foo \ :literal:`bar` (`link <parameter-bar_>`_)\ 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This lookup plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

To install it, use: :code:`ansible-galaxy collection install ns2.col`.

To use it in a playbook, specify: :code:`ns2.col.foo`.

New in ns2.col 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This looks up some foo.
- Whatever that is.






Terms
-----

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-_terms:

      **Terms**

      :literal:`list` / :literal:`elements=string` / :strong:`required`




      .. raw:: html

        </div></div>

    - 
      The stuff to look up.







Keyword parameters
------------------

This describes keyword parameters of the lookup. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
examples: ``lookup('ns2.col.foo', key1=value1, key2=value2, ...)`` and ``query('ns2.col.foo', key1=value1, key2=value2, ...)``

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
      Foo bar.





Notes
-----

- When keyword and positional parameters are used together, positional parameters must be listed before keyword parameters:
  ``lookup('ns2.col.foo', term1, term2, key1=value1, key2=value2)`` and ``query('ns2.col.foo', term1, term2, key1=value1, key2=value2)``


Examples
--------

.. code-block:: yaml

    
    - name: Look up bar
      ansible.builtin.debug:
        msg: "{{ lookup('ns2.col.foo', 'bar') }}"





Return Value
------------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _return-_raw:

      **Return value**

      :literal:`list` / :literal:`elements=string`

      .. raw:: html

        </div></div>
    - 
      The resulting stuff.


      Returned: success




Authors
~~~~~~~

- Felix Fontein (@felixfontein)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

