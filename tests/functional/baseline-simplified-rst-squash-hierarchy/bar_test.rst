

ns2.col.bar test -- Is something a bar
++++++++++++++++++++++++++++++++++++++

.. note::
    This test plugin is part of the `ns2.col collection <https://galaxy.ansible.com/ns2/col>`_ (version 2.1.0).

    To install it, use: :code:`ansible-galaxy collection install ns2.col`.

    To use it in a playbook, specify: :code:`ns2.col.bar`.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Check whether a path is a bar.


Aliases: is_bar





Input
-----

This describes the input of the test, the value before ``is ns2.col.bar`` or ``is not ns2.col.bar``.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div style="display: flex;"><div style="flex: 1 0 auto; white-space: nowrap; margin-left: 0.25em;">

      .. _parameter-_input:

      **Input**

      :literal:`path`




      .. raw:: html

        </div></div>

    - 
      A path.










Examples
--------

.. code-block:: yaml+jinja

    is_path_bar: "{{ '/etc/hosts' is ns2.col.bar }}}"





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

      :literal:`boolean`

      .. raw:: html

        </div></div>
    - 
      Returns \ :literal:`true`\  if the path is a bar, \ :literal:`false`\  if it is not a bar.


      Returned: success




Authors
~~~~~~~

- Ansible Core


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/community.general/issues>`__
* `Homepage <https://github.com/ansible-collections/community.crypto>`__
* `Repository (Sources) <https://github.com/ansible-collections/community.internal\_test\_tools>`__
* `Submit a bug report <https://github.com/ansible-community/antsibull-docs/issues/new?assignees=&labels=&template=bug\_report.md>`__

