
.. Created with antsibull-docs <ANTSIBULL_DOCS_VERSION>

ns.col2.foo4 module -- Markup reference linting test
++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ns.col2 collection <https://galaxy.ansible.com/ui/repo/published/ns/col2/>`_ (version 0.0.1).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ns.col2`.

To use it in a playbook, specify: ``ns.col2.foo4``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------









Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-correct_array_stubs"></div>
      <p style="display: inline;"><strong>correct_array_stubs</strong></p>
      <a class="ansibleOptionLink" href="#parameter-correct_array_stubs" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ansible/builtin/iptables_module.html#parameter-tcp_flags/flags"><span class="std std-ref"><span class="pre">tcp_flags.flags[]</span></span></a></strong></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/bar_filter.html#parameter-foo"><span class="std std-ref"><span class="pre">foo</span></span></a></strong></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/bar_filter.html#parameter-foo"><span class="std std-ref"><span class="pre">foo[]</span></span></a></strong></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/foo_module.html#parameter-foo/bar"><span class="std std-ref"><span class="pre">foo[baz].bar</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ext/col/foo_module.html#return-baz"><span class="std std-ref"><span class="pre">baz</span></span></a></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ext/col/foo_module.html#return-baz"><span class="std std-ref"><span class="pre">baz[ ]</span></span></a></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/stat_module.html#return-stat"><span class="std std-ref"><span class="pre">stat[foo.bar]</span></span></a></code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-existing"></div>
      <p style="display: inline;"><strong>existing</strong></p>
      <a class="ansibleOptionLink" href="#parameter-existing" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p><a href='../../ansible/builtin/service_module.html' class='module'>ansible.builtin.service</a></p>
      <p><a href='../../ansible/builtin/pipe_lookup.html' class='module'>ansible.builtin.pipe</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ansible/builtin/file_module.html#parameter-state"><span class="std std-ref"><span class="pre">state</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/stat_module.html#return-stat/exists"><span class="std std-ref"><span class="pre">stat.exists</span></span></a></code></p>
      <p><a href='../../ns2/flatcol/foo_module.html' class='module'>ns2.flatcol.foo</a></p>
      <p><a href='../../ns2/flatcol/sub.foo2_module.html' class='module'>ns2.flatcol.sub.foo2</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/flatcol/foo_module.html#parameter-subbaz/bam"><span class="std std-ref"><span class="pre">subbaz.bam</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/flatcol/sub.foo2_module.html#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code></p>
      <p><a href='../../ns2/col/foo2_module.html' class='module'>ns2.col.foo2</a></p>
      <p><a href='../../ns2/col/foo_lookup.html' class='module'>ns2.col.foo</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/bar_filter.html#parameter-foo"><span class="std std-ref"><span class="pre">foo[-1]</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/col/bar_test.html#return-_value"><span class="std std-ref"><span class="pre">_value</span></span></a></code></p>
      <p><a href='../../ns/col2/foo2_module.html' class='module'>ns.col2.foo2</a></p>
      <p><a href='../../ns/col2/foo2_module.html' class='module'>ns.col2.foo2</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns/col2/foo2_module.html#parameter-subfoo/foo"><span class="std std-ref"><span class="pre">subfoo.foo</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns/col2/foo2_module.html#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code></p>
      <p><a href='../../ext/col/foo_module.html' class='module'>ext.col.foo</a></p>
      <p><a href='../../ext/col/bar_lookup.html' class='module'>ext.col.bar</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/foo_module.html#parameter-foo/bar"><span class="std std-ref"><span class="pre">foo[len(foo)].bar</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ext/col/foo_module.html#return-baz"><span class="std std-ref"><span class="pre">baz[]</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns/col2/foo2_module.html#parameter-subfoo/BaZ"><span class="std std-ref"><span class="pre">subfoo.BaZ</span></span></a></strong></code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-incorrect_array_stubs"></div>
      <p style="display: inline;"><strong>incorrect_array_stubs</strong></p>
      <a class="ansibleOptionLink" href="#parameter-incorrect_array_stubs" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ansible/builtin/file_module.html#parameter-state"><span class="std std-ref"><span class="pre">state[]</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/stat_module.html#return-stat/exists"><span class="std std-ref"><span class="pre">stat[foo.bar].exists</span></span></a></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/stat_module.html#return-stat/exists"><span class="std std-ref"><span class="pre">stat.exists[]</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns/col2/foo2_module.html#parameter-subfoo%255B"><span class="std std-ref"><span class="pre">subfoo[</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns/col2/foo2_module.html#return-bar"><span class="std std-ref"><span class="pre">bar[]</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/foo_module.html#parameter-foo/bar"><span class="std std-ref"><span class="pre">foo.bar</span></span></a></strong></code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-not_existing"></div>
      <p style="display: inline;"><strong>not_existing</strong></p>
      <a class="ansibleOptionLink" href="#parameter-not_existing" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p><a href='../../ansible/builtin/foobar_module.html' class='module'>ansible.builtin.foobar</a></p>
      <p><a href='../../ansible/builtin/bazbam_lookup.html' class='module'>ansible.builtin.bazbam</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ansible/builtin/file_module.html#parameter-foobarbaz"><span class="std std-ref"><span class="pre">foobarbaz</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/stat_module.html#return-baz/bam"><span class="std std-ref"><span class="pre">baz.bam[]</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ansible/builtin/foobar_module.html#parameter-state"><span class="std std-ref"><span class="pre">state</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ansible/builtin/bazbam_module.html#return-stat/exists"><span class="std std-ref"><span class="pre">stat.exists</span></span></a></code></p>
      <p><a href='../../ns2/flatcol/foobarbaz_module.html' class='module'>ns2.flatcol.foobarbaz</a></p>
      <p><a href='../../ns2/flatcol/sub.bazbam_module.html' class='module'>ns2.flatcol.sub.bazbam</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/flatcol/foo_module.html#parameter-foofoofoobar"><span class="std std-ref"><span class="pre">foofoofoobar</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/flatcol/sub.foo2_module.html#return-bazbarbam"><span class="std std-ref"><span class="pre">bazbarbam</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/flatcol/foobar_module.html#parameter-subbaz/bam"><span class="std std-ref"><span class="pre">subbaz.bam</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/flatcol/sub.bazbam_module.html#return-bar"><span class="std std-ref"><span class="pre">bar</span></span></a></code></p>
      <p><a href='../../ns2/col/joo_module.html' class='module'>ns2.col.joo</a></p>
      <p><a href='../../ns2/col/joo_lookup.html' class='module'>ns2.col.joo</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/bar_filter.html#parameter-jooo"><span class="std std-ref"><span class="pre">jooo</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/col/bar_test.html#return-booo"><span class="std std-ref"><span class="pre">booo</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns2/col/joo_filter.html#parameter-foo"><span class="std std-ref"><span class="pre">foo[-1]</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns2/col/joo_test.html#return-_value"><span class="std std-ref"><span class="pre">_value</span></span></a></code></p>
      <p><a href='../../ns/col2/foobarbaz_module.html' class='module'>ns.col2.foobarbaz</a></p>
      <p><a href='../../ns/col2/foobarbam_filter.html' class='module'>ns.col2.foobarbam</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns/col2/foo2_module.html#parameter-barbazbam/foo"><span class="std std-ref"><span class="pre">barbazbam.foo</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns/col2/foo2_module.html#return-bambazbar"><span class="std std-ref"><span class="pre">bambazbar</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ns/col2/foofoo_test.html#parameter-subfoo/foo"><span class="std std-ref"><span class="pre">subfoo.foo</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ns/col2/foofoo_lookup.html#return-baz"><span class="std std-ref"><span class="pre">baz</span></span></a></code></p>
      <p><a href='../../ext/col/notthere_module.html' class='module'>ext.col.notthere</a></p>
      <p><a href='../../ext/col/notthere_lookup.html' class='module'>ext.col.notthere</a></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/foo_module.html#parameter-foo/notthere"><span class="std std-ref"><span class="pre">foo[len(foo)].notthere</span></span></a></strong></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/foo_module.html#parameter-notthere/bar"><span class="std std-ref"><span class="pre">notthere[len(notthere)].bar</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ext/col/foo_module.html#return-notthere"><span class="std std-ref"><span class="pre">notthere[]</span></span></a></code></p>
      <p><code class="ansible-option literal notranslate"><strong><a class="reference internal" href="../../ext/col/notthere_module.html#parameter-foo/bar"><span class="std std-ref"><span class="pre">foo[len(foo)].bar</span></span></a></strong></code></p>
      <p><code class="ansible-return-value literal notranslate"><a class="reference internal" href="../../ext/col/notthere_module.html#return-baz"><span class="std std-ref"><span class="pre">baz[]</span></span></a></code></p>
    </td>
  </tr>
  </tbody>
  </table>











Authors
~~~~~~~

- Nobody (@ansible)




