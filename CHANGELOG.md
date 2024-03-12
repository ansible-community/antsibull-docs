# antsibull\-docs \-\- Ansible Documentation Build Scripts Release Notes

**Topics**
- <a href="#v2-8-0">v2\.8\.0</a>
  - <a href="#release-summary">Release Summary</a>
  - <a href="#minor-changes">Minor Changes</a>
  - <a href="#bugfixes">Bugfixes</a>
- <a href="#v2-7-0">v2\.7\.0</a>
  - <a href="#release-summary-1">Release Summary</a>
  - <a href="#minor-changes-1">Minor Changes</a>
  - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v2-6-1">v2\.6\.1</a>
  - <a href="#release-summary-2">Release Summary</a>
  - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v2-6-0">v2\.6\.0</a>
  - <a href="#release-summary-3">Release Summary</a>
  - <a href="#minor-changes-2">Minor Changes</a>
  - <a href="#bugfixes-3">Bugfixes</a>
- <a href="#v2-5-0">v2\.5\.0</a>
  - <a href="#release-summary-4">Release Summary</a>
  - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v2-4-0">v2\.4\.0</a>
  - <a href="#release-summary-5">Release Summary</a>
  - <a href="#minor-changes-4">Minor Changes</a>
  - <a href="#deprecated-features">Deprecated Features</a>
  - <a href="#bugfixes-4">Bugfixes</a>
  - <a href="#known-issues">Known Issues</a>
- <a href="#v2-3-1">v2\.3\.1</a>
  - <a href="#release-summary-6">Release Summary</a>
  - <a href="#bugfixes-5">Bugfixes</a>
- <a href="#v2-3-0">v2\.3\.0</a>
  - <a href="#release-summary-7">Release Summary</a>
  - <a href="#minor-changes-5">Minor Changes</a>
  - <a href="#bugfixes-6">Bugfixes</a>
- <a href="#v2-2-0">v2\.2\.0</a>
  - <a href="#release-summary-8">Release Summary</a>
  - <a href="#minor-changes-6">Minor Changes</a>
  - <a href="#bugfixes-7">Bugfixes</a>
- <a href="#v2-1-0">v2\.1\.0</a>
  - <a href="#release-summary-9">Release Summary</a>
  - <a href="#minor-changes-7">Minor Changes</a>
  - <a href="#bugfixes-8">Bugfixes</a>
- <a href="#v2-0-0">v2\.0\.0</a>
  - <a href="#release-summary-10">Release Summary</a>
  - <a href="#major-changes">Major Changes</a>
  - <a href="#minor-changes-8">Minor Changes</a>
  - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
  - <a href="#bugfixes-9">Bugfixes</a>
- <a href="#v1-11-0">v1\.11\.0</a>
  - <a href="#release-summary-11">Release Summary</a>
  - <a href="#minor-changes-9">Minor Changes</a>
- <a href="#v1-10-0">v1\.10\.0</a>
  - <a href="#release-summary-12">Release Summary</a>
  - <a href="#major-changes-1">Major Changes</a>
  - <a href="#minor-changes-10">Minor Changes</a>
  - <a href="#bugfixes-10">Bugfixes</a>
- <a href="#v1-9-0">v1\.9\.0</a>
  - <a href="#release-summary-13">Release Summary</a>
  - <a href="#minor-changes-11">Minor Changes</a>
- <a href="#v1-8-2">v1\.8\.2</a>
  - <a href="#release-summary-14">Release Summary</a>
  - <a href="#bugfixes-11">Bugfixes</a>
- <a href="#v1-8-1">v1\.8\.1</a>
  - <a href="#release-summary-15">Release Summary</a>
  - <a href="#bugfixes-12">Bugfixes</a>
- <a href="#v1-8-0">v1\.8\.0</a>
  - <a href="#release-summary-16">Release Summary</a>
  - <a href="#minor-changes-12">Minor Changes</a>
  - <a href="#bugfixes-13">Bugfixes</a>
- <a href="#v1-7-4">v1\.7\.4</a>
  - <a href="#release-summary-17">Release Summary</a>
  - <a href="#bugfixes-14">Bugfixes</a>
- <a href="#v1-7-3">v1\.7\.3</a>
  - <a href="#release-summary-18">Release Summary</a>
  - <a href="#bugfixes-15">Bugfixes</a>
- <a href="#v1-7-2">v1\.7\.2</a>
  - <a href="#release-summary-19">Release Summary</a>
  - <a href="#bugfixes-16">Bugfixes</a>
- <a href="#v1-7-1">v1\.7\.1</a>
  - <a href="#release-summary-20">Release Summary</a>
  - <a href="#bugfixes-17">Bugfixes</a>
- <a href="#v1-7-0">v1\.7\.0</a>
  - <a href="#release-summary-21">Release Summary</a>
  - <a href="#minor-changes-13">Minor Changes</a>
  - <a href="#bugfixes-18">Bugfixes</a>
- <a href="#v1-6-1">v1\.6\.1</a>
  - <a href="#release-summary-22">Release Summary</a>
  - <a href="#bugfixes-19">Bugfixes</a>
- <a href="#v1-6-0">v1\.6\.0</a>
  - <a href="#release-summary-23">Release Summary</a>
  - <a href="#minor-changes-14">Minor Changes</a>
  - <a href="#bugfixes-20">Bugfixes</a>
- <a href="#v1-5-0">v1\.5\.0</a>
  - <a href="#release-summary-24">Release Summary</a>
  - <a href="#minor-changes-15">Minor Changes</a>
  - <a href="#bugfixes-21">Bugfixes</a>
- <a href="#v1-4-0">v1\.4\.0</a>
  - <a href="#release-summary-25">Release Summary</a>
  - <a href="#minor-changes-16">Minor Changes</a>
  - <a href="#bugfixes-22">Bugfixes</a>
- <a href="#v1-3-0">v1\.3\.0</a>
  - <a href="#release-summary-26">Release Summary</a>
  - <a href="#minor-changes-17">Minor Changes</a>
  - <a href="#bugfixes-23">Bugfixes</a>
- <a href="#v1-2-2">v1\.2\.2</a>
  - <a href="#release-summary-27">Release Summary</a>
  - <a href="#bugfixes-24">Bugfixes</a>
- <a href="#v1-2-1">v1\.2\.1</a>
  - <a href="#release-summary-28">Release Summary</a>
  - <a href="#bugfixes-25">Bugfixes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
  - <a href="#release-summary-29">Release Summary</a>
  - <a href="#minor-changes-18">Minor Changes</a>
  - <a href="#bugfixes-26">Bugfixes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
  - <a href="#release-summary-30">Release Summary</a>
  - <a href="#minor-changes-19">Minor Changes</a>
- <a href="#v1-0-1">v1\.0\.1</a>
  - <a href="#release-summary-31">Release Summary</a>
  - <a href="#bugfixes-27">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
  - <a href="#release-summary-32">Release Summary</a>
  - <a href="#major-changes-2">Major Changes</a>
  - <a href="#minor-changes-20">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
  - <a href="#release-summary-33">Release Summary</a>

<a id="v2-8-0"></a>
## v2\.8\.0

<a id="release-summary"></a>
### Release Summary

Bugfix and feature release\.

<a id="minor-changes"></a>
### Minor Changes

* Add support for \"dark mode\" to the option table styling \([https\://github\.com/ansible\-community/antsibull\-docs/pull/253](https\://github\.com/ansible\-community/antsibull\-docs/pull/253)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/258](https\://github\.com/ansible\-community/antsibull\-docs/pull/258)\)\.
* Add support for the latest antsibull\-core v3 pre\-release\, <code>3\.0\.0a1</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/250](https\://github\.com/ansible\-community/antsibull\-docs/pull/250)\)\.
* Declare support for Python 3\.12 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/255](https\://github\.com/ansible\-community/antsibull\-docs/pull/255)\)\.
* The colors used by the CSS provided by the Antsibull Sphinx extension can now be overridden \([https\://github\.com/ansible\-community/antsibull\-docs/pull/254](https\://github\.com/ansible\-community/antsibull\-docs/pull/254)\)\.

<a id="bugfixes"></a>
### Bugfixes

* Fix duplicate docs detection \(for aliases\) for latest ansible\-core devel \([https\://github\.com/ansible\-community/antsibull\-docs/pull/257](https\://github\.com/ansible\-community/antsibull\-docs/pull/257)\)\.

<a id="v2-7-0"></a>
## v2\.7\.0

<a id="release-summary-1"></a>
### Release Summary

Bugfix and refactoring release\.

<a id="minor-changes-1"></a>
### Minor Changes

* Explicitly set up Galaxy context instead of relying on deprecated functionality \([https\://github\.com/ansible\-community/antsibull\-docs/pull/234](https\://github\.com/ansible\-community/antsibull\-docs/pull/234)\)\.

<a id="bugfixes-1"></a>
### Bugfixes

* Fix schema for <code>seealso</code> in role entrypoints\. Plugin references now work \([https\://github\.com/ansible\-community/antsibull\-docs/issues/237](https\://github\.com/ansible\-community/antsibull\-docs/issues/237)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/240](https\://github\.com/ansible\-community/antsibull\-docs/pull/240)\)\.
* Make error reporting for invalid references in <code>plugin</code> <code>seealso</code> entries more precise \([https\://github\.com/ansible\-community/antsibull\-docs/pull/240](https\://github\.com/ansible\-community/antsibull\-docs/pull/240)\)\.
* Support new <code>ansible\-doc \-\-json</code> output field <code>plugin\_name</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/242](https\://github\.com/ansible\-community/antsibull\-docs/pull/242)\)\.
* Use certain fields from library context instead of app context that are deprecated in the app context and will be removed from antsibull\-core 3\.0\.0 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/233](https\://github\.com/ansible\-community/antsibull\-docs/pull/233)\)\.

<a id="v2-6-1"></a>
## v2\.6\.1

<a id="release-summary-2"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-2"></a>
### Bugfixes

* For role argument specs\, allow <code>author</code>\, <code>description</code>\, and <code>todo</code> to be a string instead of a list of strings\, similarly as with ansible\-doc and with modules and plugins \([https\://github\.com/ansible\-community/antsibull\-docs/pull/227](https\://github\.com/ansible\-community/antsibull\-docs/pull/227)\)\.
* Make sure that title underlines have the correct width for wide Unicode characters \([https\://github\.com/ansible\-community/antsibull\-docs/issues/228](https\://github\.com/ansible\-community/antsibull\-docs/issues/228)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/229](https\://github\.com/ansible\-community/antsibull\-docs/pull/229)\)\.

<a id="v2-6-0"></a>
## v2\.6\.0

<a id="release-summary-3"></a>
### Release Summary

Fix parsing of <code>EXAMPLES</code> and improve error message

<a id="minor-changes-2"></a>
### Minor Changes

* Improve error messages when calls to <code>ansible\-doc</code> fail \([https\://github\.com/ansible\-community/antsibull\-docs/pull/223](https\://github\.com/ansible\-community/antsibull\-docs/pull/223)\)\.

<a id="bugfixes-3"></a>
### Bugfixes

* When <code>EXAMPLES</code> has the format specified by <code>\# fmt\: \<format\></code>\, this value is used to determine the code block type \([https\://github\.com/ansible\-community/antsibull\-docs/pull/225](https\://github\.com/ansible\-community/antsibull\-docs/pull/225)\)\.

<a id="v2-5-0"></a>
## v2\.5\.0

<a id="release-summary-4"></a>
### Release Summary

Release to support the updated Ansible Galaxy codebase\.

<a id="minor-changes-3"></a>
### Minor Changes

* The default collection URL template has been changed from <code>https\://galaxy\.ansible\.com/\{namespace\}/\{name\}</code> to <code>https\://galaxy\.ansible\.com/ui/repo/published/\{namespace\}/\{name\}/</code> to adjust for the Galaxy codebase change on September 30th\, 2023 \([https\://github\.com/ansible\-community/antsibull\-docs/issues/147](https\://github\.com/ansible\-community/antsibull\-docs/issues/147)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/220](https\://github\.com/ansible\-community/antsibull\-docs/pull/220)\)\.

<a id="v2-4-0"></a>
## v2\.4\.0

<a id="release-summary-5"></a>
### Release Summary

Bugfix and feature release\. Improves support for other builders than <code>html</code>\.

There will be a follow\-up release after [Ansible Galaxy](https\://galaxy\.ansible\.com/)
switched to the new <code>galaxy\_ng</code> codebase\, which is scheduled for September 30th\.
That release will only adjust the URLs to Galaxy\, except potentially bugfixes\.

<a id="minor-changes-4"></a>
### Minor Changes

* Add basic support for other HTML based Sphinx builders such as <code>epub</code> and <code>singlehtml</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/201](https\://github\.com/ansible\-community/antsibull\-docs/pull/201)\)\.
* Adjust default RST output to work better with Spinx\'s LaTeX builder \([https\://github\.com/ansible\-community/antsibull\-docs/pull/195](https\://github\.com/ansible\-community/antsibull\-docs/pull/195)\)\.
* Allow specifying wildcards for the collection names for the <code>collections</code> subcommand if <code>\-\-use\-current</code> is specified \([https\://github\.com/ansible\-community/antsibull\-docs/pull/219](https\://github\.com/ansible\-community/antsibull\-docs/pull/219)\)\.
* Antsibull\-docs now depends on antsibull\-core \>\= 2\.1\.0 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/209](https\://github\.com/ansible\-community/antsibull\-docs/pull/209)\)\.
* Create collection links with a custom directive\. This makes them compatible with builders other than the HTML builder \([https\://github\.com/ansible\-community/antsibull\-docs/pull/200](https\://github\.com/ansible\-community/antsibull\-docs/pull/200)\)\.
* Fix indent for nested options and return values with Spinx\'s LaTeX builder \([https\://github\.com/ansible\-community/antsibull\-docs/pull/198](https\://github\.com/ansible\-community/antsibull\-docs/pull/198)\)\.
* Improve linting of option and return value names in semantic markup with respect to array stubs\: forbid array stubs for dictionaries if the dictionary is not the last part of the option \([https\://github\.com/ansible\-community/antsibull\-docs/pull/208](https\://github\.com/ansible\-community/antsibull\-docs/pull/208)\)\.
* Improve the info box for <code>ansible\.builtin</code> plugins and modules to explain FQCN and link to the <code>collection</code> keyword docs \([https\://github\.com/ansible\-community/antsibull\-docs/pull/218](https\://github\.com/ansible\-community/antsibull\-docs/pull/218)\)\.
* Improve the info box for modules\, plugins\, and roles in collections to show note that they are not included in <code>ansible\-core</code> and show instructions on how to check whether the collection is installed \([https\://github\.com/ansible\-community/antsibull\-docs/pull/218](https\://github\.com/ansible\-community/antsibull\-docs/pull/218)\)\.
* Insert the antsibull\-docs version as a comment or metadata into the generated files \([https\://github\.com/ansible\-community/antsibull\-docs/pull/205](https\://github\.com/ansible\-community/antsibull\-docs/pull/205)\)\.
* Make sure that the antsibull Sphinx extension contains the correct version \(same as antsibull\-docs itself\) and licensing information \(GPL\-3\.0\-or\-later\)\, and that the version is kept up\-to\-date for new releases \([https\://github\.com/ansible\-community/antsibull\-docs/pull/202](https\://github\.com/ansible\-community/antsibull\-docs/pull/202)\)\.
* Move roles from templates and structural styling from stylesheet to antsibull Sphinx extension\. This makes sure that HTML tags such as <code>\<strong\></code> and <code>\<em\></code> are used for bold and italic texts\, and that the same formattings are used for the LaTeX builder \([https\://github\.com/ansible\-community/antsibull\-docs/pull/199](https\://github\.com/ansible\-community/antsibull\-docs/pull/199)\)\.
* Support multiple filters in <code>ansible\-doc</code> of ansible\-core 2\.16 and later\. This makes building docsites and linting more efficient when documentation for more than one and less than all installed collections needs to be queried \([https\://github\.com/ansible\-community/antsibull\-docs/issues/193](https\://github\.com/ansible\-community/antsibull\-docs/issues/193)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/213](https\://github\.com/ansible\-community/antsibull\-docs/pull/213)\)\.
* The <code>current</code> subcommand now has a <code>\-\-skip\-ansible\-builtin</code> option which skips building documentation for <code>ansible\.builtin</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/215](https\://github\.com/ansible\-community/antsibull\-docs/pull/215)\)\.
* Use same colors for LaTeX builder\'s output as for HTML builder\'s output \([https\://github\.com/ansible\-community/antsibull\-docs/pull/199](https\://github\.com/ansible\-community/antsibull\-docs/pull/199)\)\.

<a id="deprecated-features"></a>
### Deprecated Features

* The <code>\-\-use\-html\-blobs</code> feature that inserts HTML blobs for the options and return value tables for the <code>ansible\-docsite</code> output format is deprecated and will be removed soon\. The HTML tables cause several features to break\, such as references to options and return values\. If you think this feature needs to stay\, please create an issue in the [antsibull\-docs repository](https\://github\.com/ansible\-community/antsibull\-docs/issues/) and provide good reasons for it \([https\://github\.com/ansible\-community/antsibull\-docs/pull/217](https\://github\.com/ansible\-community/antsibull\-docs/pull/217)\)\.

<a id="bugfixes-4"></a>
### Bugfixes

* Document and ensure that the <code>collection</code> subcommand with <code>\-\-use\-current</code> can only be used with collection names \([https\://github\.com/ansible\-community/antsibull\-docs/pull/214](https\://github\.com/ansible\-community/antsibull\-docs/pull/214)\)\.
* Fix FQCN detection \([https\://github\.com/ansible\-community/antsibull\-docs/pull/214](https\://github\.com/ansible\-community/antsibull\-docs/pull/214)\)\.
* The <code>collection</code> subcommand claimed to support paths to directories\, which was never supported\. Removed the mention of paths from the help\, and added validation \([https\://github\.com/ansible\-community/antsibull\-docs/pull/214](https\://github\.com/ansible\-community/antsibull\-docs/pull/214)\)\.
* The <code>plugin</code> subcommand claimed to support paths to plugin files\, which was never supported\. Removed the mention of paths from the help \([https\://github\.com/ansible\-community/antsibull\-docs/pull/214](https\://github\.com/ansible\-community/antsibull\-docs/pull/214)\)\.
* When running <code>antsibull\-docs \-\-help</code>\, the correct program name is now shown for the <code>\-\-version</code> option \([https\://github\.com/ansible\-community/antsibull\-docs/pull/209](https\://github\.com/ansible\-community/antsibull\-docs/pull/209)\)\.
* When running <code>antsibull\-docs \-\-version</code>\, the correct version is now shown also for editable installs and other installs that do not allow <code>importlib\.metadata</code> to show the correct version \([https\://github\.com/ansible\-community/antsibull\-docs/pull/209](https\://github\.com/ansible\-community/antsibull\-docs/pull/209)\)\.
* When using the <code>action\_group</code> or <code>platform</code> attributes in a role\, a RST symbol was used that was not defined \([https\://github\.com/ansible\-community/antsibull\-docs/pull/206](https\://github\.com/ansible\-community/antsibull\-docs/pull/206)\)\.

<a id="known-issues"></a>
### Known Issues

* When using Sphinx builders other than HTML and LaTeX\, the indentation for nested options and return values is missing \([https\://github\.com/ansible\-community/antsibull\-docs/pull/195](https\://github\.com/ansible\-community/antsibull\-docs/pull/195)\)\.

<a id="v2-3-1"></a>
## v2\.3\.1

<a id="release-summary-6"></a>
### Release Summary

Bugfix release with a CSS fix for the Sphinx extension\.

<a id="bugfixes-5"></a>
### Bugfixes

* Fix antsibull Sphinx extension CSS so that the option/return value anchors for module/plugin/role documentation can also be used on WebKit\-based browsers such as Gnome Web and Safari \([https\://github\.com/ansible\-community/antsibull\-docs/issues/188](https\://github\.com/ansible\-community/antsibull\-docs/issues/188)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/189](https\://github\.com/ansible\-community/antsibull\-docs/pull/189)\)\.

<a id="v2-3-0"></a>
## v2\.3\.0

<a id="release-summary-7"></a>
### Release Summary

Bugfix and feature release\.

<a id="minor-changes-5"></a>
### Minor Changes

* Add a <code>\:ansplugin\:</code> role to the Sphinx extension\. This allows to reference a module\, plugin\, or role with the <code>fqcn\#type</code> syntax from semantic markup instead of having to manually compose a <code>ansible\_collections\.\{fqcn\}\_\{type\}</code> label\. An explicit reference title can also be provided with the <code>title \<fqcn\#type\></code> syntax similar to the <code>\:ref\:</code> role \([https\://github\.com/ansible\-community/antsibull\-docs/pull/180](https\://github\.com/ansible\-community/antsibull\-docs/pull/180)\)\.
* Add a new subcommand <code>lint\-core\-docs</code> which lints the ansible\-core documentation \([https\://github\.com/ansible\-community/antsibull\-docs/pull/182](https\://github\.com/ansible\-community/antsibull\-docs/pull/182)\)\.
* Add a new subcommand\, <code>collection\-plugins</code>\, for rendering files for all plugins and roles in a collection without any indexes \([https\://github\.com/ansible\-community/antsibull\-docs/pull/177](https\://github\.com/ansible\-community/antsibull\-docs/pull/177)\)\.
* Add support for different output formats\. Next to the default format\, <code>ansible\-docsite</code>\, a new <strong>experimental</strong> format <code>simplified\-rst</code> is supported\. Experimental means that it will likely change considerably in the next few releases until it stabilizes\. Such changes will not be considered breaking changes\, and could potentially even be bugfixes \([https\://github\.com/ansible\-community/antsibull\-docs/pull/177](https\://github\.com/ansible\-community/antsibull\-docs/pull/177)\)\.
* Use Dart sass compiler instead of sassc to compile CSS for Sphinx extension \([https\://github\.com/ansible\-community/antsibull\-docs/issues/185](https\://github\.com/ansible\-community/antsibull\-docs/issues/185)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/186](https\://github\.com/ansible\-community/antsibull\-docs/pull/186)\)\.
* When parsing errors happen in the Sphinx extension\, the extension now emits error messages during the build process in addition to error markup \([https\://github\.com/ansible\-community/antsibull\-docs/pull/187](https\://github\.com/ansible\-community/antsibull\-docs/pull/187)\)\.

<a id="bugfixes-6"></a>
### Bugfixes

* Consider module/plugin aliases when linting references to other modules and plugins \([https\://github\.com/ansible\-community/antsibull\-docs/pull/184](https\://github\.com/ansible\-community/antsibull\-docs/pull/184)\)\.
* Make sure that all aliases are actually listed for plugins \([https\://github\.com/ansible\-community/antsibull\-docs/pull/183](https\://github\.com/ansible\-community/antsibull\-docs/pull/183)\)\.
* When looking for redirects\, the <code>aliases</code> field and filesystem redirects in ansible\-core were not properly considered\. This ensures that all redirect stubs are created\, and that no duplicates show up\, not depending on whether ansible\-core is installed in editable mode or not \([https\://github\.com/ansible\-community/antsibull\-docs/pull/183](https\://github\.com/ansible\-community/antsibull\-docs/pull/183)\)\.

<a id="v2-2-0"></a>
## v2\.2\.0

<a id="release-summary-8"></a>
### Release Summary

Bugfix and feature release improving rendering and linting\.

<a id="minor-changes-6"></a>
### Minor Changes

* Collection docs linter \- also validate <code>seealso</code> module and plugin destinations \([https\://github\.com/ansible\-community/antsibull\-docs/issues/168](https\://github\.com/ansible\-community/antsibull\-docs/issues/168)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/171](https\://github\.com/ansible\-community/antsibull\-docs/pull/171)\)\.
* When linting collection plugin docs\, make sure that array stubs <code>\[\.\.\.\]</code> are used when referencing sub\-options or sub\-return values inside lists\, and are not used outside lists and dictionaries \([https\://github\.com/ansible\-community/antsibull\-docs/pull/173](https\://github\.com/ansible\-community/antsibull\-docs/pull/173)\)\.

<a id="bugfixes-7"></a>
### Bugfixes

* Fix the way the Sphinx extension creates nodes for options and return values so they look identical for internal references\, external \(intersphinx\) references\, and unresolved references \([https\://github\.com/ansible\-community/antsibull\-docs/pull/175](https\://github\.com/ansible\-community/antsibull\-docs/pull/175)\)\.
* Make sure that <code>\:ansopt\:</code> and <code>\:ansretval\:</code> create the same references as the labels created in the RST files \([https\://github\.com/ansible\-community/antsibull\-docs/issues/167](https\://github\.com/ansible\-community/antsibull\-docs/issues/167)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/172](https\://github\.com/ansible\-community/antsibull\-docs/pull/172)\)\.
* Make sure that broken <code>\:ansopt\:</code> and <code>\:ansretval\:</code> parameters result in correctly rendered error messages \([https\://github\.com/ansible\-community/antsibull\-docs/pull/175](https\://github\.com/ansible\-community/antsibull\-docs/pull/175)\)\.
* When trying to copying descriptions of non\-existing plugins to <code>seealso</code>\, references to these non\-existing plugins were added in some cases\, crashing the docs augmentation process \([https\://github\.com/ansible\-community/antsibull\-docs/pull/169](https\://github\.com/ansible\-community/antsibull\-docs/pull/169)\)\.

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="release-summary-9"></a>
### Release Summary

Feature and bugfix release with many improvements related to semantic markup and validation\.

<a id="minor-changes-7"></a>
### Minor Changes

* Add option <code>\-\-disallow\-unknown\-collection\-refs</code> to disallow references to other collections than the one covered by <code>\-\-validate\-collection\-refs</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/157](https\://github\.com/ansible\-community/antsibull\-docs/pull/157)\)\.
* Add option <code>\-\-validate\-collection\-refs</code> to the <code>lint\-collection\-docs</code> subcommand to also control which references to plugin/module/role names in \(other\) collections and their options and return values should be validated \([https\://github\.com/ansible\-community/antsibull\-docs/pull/157](https\://github\.com/ansible\-community/antsibull\-docs/pull/157)\)\.
* Add the new collection config field <code>envvar\_directives</code> which allows to declare which environment variables are declared with an <code>\.\. envvar\:\:</code> directive in the collection\'s extra docsite documentation\. This is used\, next to the plugin configuration information and the ansible\-core configuration information\, to determine whether an environment variable is referencable or not \([https\://github\.com/ansible\-community/antsibull\-docs/pull/166](https\://github\.com/ansible\-community/antsibull\-docs/pull/166)\)\.
* Add the roles <code>\:ansenvvar\:</code> and <code>\:ansenvvarref\:</code> to the antsibull\-docs Sphinx extension \([https\://github\.com/ansible\-community/antsibull\-docs/pull/166](https\://github\.com/ansible\-community/antsibull\-docs/pull/166)\)\.
* Render <code>E\(\.\.\.\)</code> markup with <code>\:ansenvvarref\:</code> or <code>\:ansenvvar\:</code> depending on whether the environment variable is known to be referencable or not \([https\://github\.com/ansible\-community/antsibull\-docs/pull/166](https\://github\.com/ansible\-community/antsibull\-docs/pull/166)\)\.
* When linting markup in collection docs\, validate plugin/module/role names\, and also option/return value names for other plugins/modules/roles in the same collection\, \(transitively\) dependent collections\, and ansible\.builtin \([https\://github\.com/ansible\-community/antsibull\-docs/pull/157](https\://github\.com/ansible\-community/antsibull\-docs/pull/157)\)\.
* When linting semantic markup in collection docs\, also accept aliases when checking <code>O\(\)</code> values \([https\://github\.com/ansible\-community/antsibull\-docs/pull/155](https\://github\.com/ansible\-community/antsibull\-docs/pull/155)\)\.
* When refering to markup in multi\-paragraph texts\, like <code>description</code>\, now includes the paragraph number in error messages \([https\://github\.com/ansible\-community/antsibull\-docs/pull/163](https\://github\.com/ansible\-community/antsibull\-docs/pull/163)\)\.

<a id="bugfixes-8"></a>
### Bugfixes

* Allow role entrypoint deprecations without having to specify the collection the role is removed from \([https\://github\.com/ansible\-community/antsibull\-docs/pull/156](https\://github\.com/ansible\-community/antsibull\-docs/pull/156)\)\.
* Indent module/plugin and role entrypoint deprecations correctly if \'Why\' or \'Alternative\' texts need more than one line \([https\://github\.com/ansible\-community/antsibull\-docs/pull/156](https\://github\.com/ansible\-community/antsibull\-docs/pull/156)\)\.
* When collecting collection dependencies for the <code>lint\-collection\-docs</code> subcommand\, a bug prevented the duplicate detection to work \([https\://github\.com/ansible\-community/antsibull\-docs/pull/160](https\://github\.com/ansible\-community/antsibull\-docs/pull/160)\)\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="release-summary-10"></a>
### Release Summary

Major new release that drops support for older Python and Ansible/ansible\-base/ansible\-core versions\.

<a id="major-changes"></a>
### Major Changes

* Change pyproject build backend from <code>poetry\-core</code> to <code>hatchling</code>\. <code>pip install antsibull\-docs</code> works exactly the same as before\, but some users may be affected depending on how they build/install the project \([https\://github\.com/ansible\-community/antsibull\-docs/pull/115](https\://github\.com/ansible\-community/antsibull\-docs/pull/115)\)\.

<a id="minor-changes-8"></a>
### Minor Changes

* Allow to use the currently installed ansible\-core version for the <code>devel</code> and <code>stable</code> subcommands \([https\://github\.com/ansible\-community/antsibull\-docs/pull/121](https\://github\.com/ansible\-community/antsibull\-docs/pull/121)\)\.
* Ansibull\-docs now no longer depends directly on <code>sh</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/122](https\://github\.com/ansible\-community/antsibull\-docs/pull/122)\)\.
* Bump version range of antsibull\-docs requirement written by <code>sphinx\-init</code> subcommand to <code>\>\= 2\.0\.0\, \< 3\.0\.0</code>\. Previously\, this was set to <code>\>\=2\.0\.0a2\, \<3\.0\.0</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/151](https\://github\.com/ansible\-community/antsibull\-docs/pull/151)\)\.
* Now depends antsibull\-core 2\.0\.0 or newer\; antsibull\-core 1\.x\.y is no longer supported \([https\://github\.com/ansible\-community/antsibull\-docs/pull/122](https\://github\.com/ansible\-community/antsibull\-docs/pull/122)\)\.
* Remove residual compatability code for Python 3\.6 and 3\.7 \([https\://github\.com/ansible\-community/antsibull\-docs/pulls/70](https\://github\.com/ansible\-community/antsibull\-docs/pulls/70)\)\.
* Support a per\-collection docs config file <code>docs/docsite/config\.yml</code>\. It is also linted by the <code>lint\-collection\-docs</code> subcommand \([https\://github\.com/ansible\-community/antsibull\-docs/pull/134](https\://github\.com/ansible\-community/antsibull\-docs/pull/134)\)\.
* The antsibull\-docs requirement in the <code>requirements\.txt</code> file created by the sphinx\-init subcommand now has version range <code>\>\= 2\.0\.0\, \< 3\.0\.0</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/126](https\://github\.com/ansible\-community/antsibull\-docs/pull/126)\)\.
* The dependency [antsibull\-docs\-parser](https\://github\.com/ansible\-community/antsibull\-docs\-parser) has been added and is used for processing Ansible markup \([https\://github\.com/ansible\-community/antsibull\-docs/pull/124](https\://github\.com/ansible\-community/antsibull\-docs/pull/124)\)\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* Disable flatmapping for all collections except community\.general \< 6\.0\.0 and community\.network \< 5\.0\.0\. You can enable flatmapping for your collection by setting <code>flatmap\: true</code> in <code>docs/docsite/config\.yml</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/134](https\://github\.com/ansible\-community/antsibull\-docs/pull/134)\)\.
* Drop support for Python 3\.6\, 3\.7\, and 3\.8 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/115](https\://github\.com/ansible\-community/antsibull\-docs/pull/115)\)\.\"
* No longer removes <code>PYTHONPATH</code> from the environment when calling <code>ansible</code>\, <code>ansible\-galaxy</code>\, or <code>ansible\-doc</code> outside a self\-created venv \([https\://github\.com/ansible\-community/antsibull\-docs/pull/121](https\://github\.com/ansible\-community/antsibull\-docs/pull/121)\)\.
* No longer supports Ansible 2\.9\, ansible\-base 2\.10\, and ansible\-core 2\.11 and 2\.12\. The minimum required ansible\-core version is 2\.13\. This allows for simpler and more efficient docs parsing and information retrieval \([https\://github\.com/ansible\-community/antsibull\-docs/pull/120](https\://github\.com/ansible\-community/antsibull\-docs/pull/120)\)\.
* The <code>ansible\-doc</code> and <code>ansible\-internal</code> values for <code>doc\_parsing\_backend</code> in the configuration file have been removed\. Change the value to <code>auto</code> for best compatibility \([https\://github\.com/ansible\-community/antsibull\-docs/pull/120](https\://github\.com/ansible\-community/antsibull\-docs/pull/120)\)\.

<a id="bugfixes-9"></a>
### Bugfixes

* Bump version range of antsibull\-docs requirement written by <code>sphinx\-init</code> subcommand to <code>\>\= 2\.0\.0a2\, \< 3\.0\.0</code>\. Previously\, this was set to <code>\>\=2\.0\.0\, \<3\.0\.0</code> which could not be satisfied \([https\://github\.com/ansible\-community/antsibull\-docs/pull/149](https\://github\.com/ansible\-community/antsibull\-docs/pull/149)\)\.
* Use <code>doc\_parsing\_backend</code> from the application context instead of the library context\. This prevents removal of <code>doc\_parsing\_backend</code> from the antsibull\-core library context \([https\://github\.com/ansible\-community/antsibull\-docs/pull/125](https\://github\.com/ansible\-community/antsibull\-docs/pull/125)\)\.

<a id="v1-11-0"></a>
## v1\.11\.0

<a id="release-summary-11"></a>
### Release Summary

Feature release\.

<a id="minor-changes-9"></a>
### Minor Changes

* Add support for semantic markup in roles \([https\://github\.com/ansible\-community/antsibull\-docs/pull/113](https\://github\.com/ansible\-community/antsibull\-docs/pull/113)\)\.
* Internal refactoring of markup code \([https\://github\.com/ansible\-community/antsibull\-docs/pull/108](https\://github\.com/ansible\-community/antsibull\-docs/pull/108)\)\.
* The <code>lint\-collection\-docs</code> subcommand can be told not to run rstcheck when <code>\-\-plugin\-docs</code> is used by passing <code>\-\-skip\-rstcheck</code>\. This speeds up testing for large collections \([https\://github\.com/ansible\-community/antsibull\-docs/pull/112](https\://github\.com/ansible\-community/antsibull\-docs/pull/112)\)\.
* The <code>lint\-collection\-docs</code> subcommand will now also validate Ansible markup when <code>\-\-plugin\-docs</code> is passed\. It can also ensure that no semantic markup is used with the new <code>\-\-disallow\-semantic\-markup</code> option\. This can for example be used by collections to avoid semantic markup being backported to older stable branches \([https\://github\.com/ansible\-community/antsibull\-docs/pull/112](https\://github\.com/ansible\-community/antsibull\-docs/pull/112)\)\.

<a id="v1-10-0"></a>
## v1\.10\.0

<a id="release-summary-12"></a>
### Release Summary

Bugfix and feature release\.

<a id="major-changes-1"></a>
### Major Changes

* Support new semantic markup in documentation \([https\://github\.com/ansible\-community/antsibull\-docs/pull/4](https\://github\.com/ansible\-community/antsibull\-docs/pull/4)\)\.

<a id="minor-changes-10"></a>
### Minor Changes

* Add a note about the ordering of positional and named parameter to the plugin page\. Also mention positional and keyword parameters for lookups \([https\://github\.com/ansible\-community/antsibull\-docs/pull/101](https\://github\.com/ansible\-community/antsibull\-docs/pull/101)\)\.
* Update schema for roles argument spec to allow specifying attributes on the entrypoint level\. These are now also rendered when present \([https\://github\.com/ansible\-community/antsibull\-docs/pull/103](https\://github\.com/ansible\-community/antsibull\-docs/pull/103)\)\.

<a id="bugfixes-10"></a>
### Bugfixes

* Explicitly declare the <code>sh</code> dependency and limit it to before 2\.0\.0\. Also explicitly declare the dependencies on <code>pydantic</code>\, <code>semantic\_version</code>\, <code>aiohttp</code>\, <code>twiggy</code>\, and <code>PyYAML</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/99](https\://github\.com/ansible\-community/antsibull\-docs/pull/99)\)\.
* Restrict the <code>pydantic</code> dependency to major version 1 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/102](https\://github\.com/ansible\-community/antsibull\-docs/pull/102)\)\.

<a id="v1-9-0"></a>
## v1\.9\.0

<a id="release-summary-13"></a>
### Release Summary

Feature release\.

<a id="minor-changes-11"></a>
### Minor Changes

* Improve build script generated by <code>antsibull\-docs sphinx\-init</code> to change to the directory where the script is located\, instead of hardcoding the script\'s path\. This also fixed the existing bug that the path was not quoted \([https\://github\.com/ansible\-community/antsibull\-docs/issues/91](https\://github\.com/ansible\-community/antsibull\-docs/issues/91)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/92](https\://github\.com/ansible\-community/antsibull\-docs/pull/92)\)\.
* Show callback plugin type on callback plugin pages\. Also write callback indexes by callback plugin type \([https\://github\.com/ansible\-community/antsibull\-docs/issues/89](https\://github\.com/ansible\-community/antsibull\-docs/issues/89)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/90](https\://github\.com/ansible\-community/antsibull\-docs/pull/90)\)\.

<a id="v1-8-2"></a>
## v1\.8\.2

<a id="release-summary-14"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-11"></a>
### Bugfixes

* Fix the new options <code>\-\-extra\-html\-context</code> and <code>\-\-extra\-html\-theme\-options</code> of the <code>sphinx\-init</code> subcommand \([https\://github\.com/ansible\-community/antsibull\-docs/pull/86](https\://github\.com/ansible\-community/antsibull\-docs/pull/86)\)\.

<a id="v1-8-1"></a>
## v1\.8\.1

<a id="release-summary-15"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-12"></a>
### Bugfixes

* When creating toctrees for breadcrumbs\, place subtree for a plugin type in the plugin type\'s section \([https\://github\.com/ansible\-community/antsibull\-docs/pull/83](https\://github\.com/ansible\-community/antsibull\-docs/pull/83)\)\.

<a id="v1-8-0"></a>
## v1\.8\.0

<a id="release-summary-16"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-12"></a>
### Minor Changes

* Add new options <code>\-\-project</code>\, <code>\-\-copyright</code>\, <code>\-\-title</code>\, <code>\-\-html\-short\-title</code>\, <code>\-\-extra\-conf</code>\, <code>\-\-extra\-html\-context</code>\, and <code>\-\-extra\-html\-theme\-options</code> to the <code>sphinx\-init</code> subcommand to allow to customize the generated <code>conf\.py</code> Sphinx configuration \([https\://github\.com/ansible\-community/antsibull\-docs/pull/77](https\://github\.com/ansible\-community/antsibull\-docs/pull/77)\)\.
* Automatically use a module\'s or plugin\'s short description as the \"See also\" description if no description is provided \([https\://github\.com/ansible\-community/antsibull\-docs/issues/64](https\://github\.com/ansible\-community/antsibull\-docs/issues/64)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/74](https\://github\.com/ansible\-community/antsibull\-docs/pull/74)\)\.
* It is now possible to provide a path to an existing file to be used as <code>rst/index\.rst</code> for <code>antsibull\-docs sphinx\-init</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/68](https\://github\.com/ansible\-community/antsibull\-docs/pull/68)\)\.
* Make compatible with antsibull\-core 2\.x\.y \([https\://github\.com/ansible\-community/antsibull\-docs/pull/78](https\://github\.com/ansible\-community/antsibull\-docs/pull/78)\)\.
* Remove support for <code>forced\_action\_plugin</code>\, a module attribute that was removed during the development phase of attributes \([https\://github\.com/ansible\-community/antsibull\-docs/pull/63](https\://github\.com/ansible\-community/antsibull\-docs/pull/63)\)\.
* Stop mentioning the version features were added for Ansible if the Ansible version is before 2\.7 \([https\://github\.com/ansible\-community/antsibull\-docs/pull/76](https\://github\.com/ansible\-community/antsibull\-docs/pull/76)\)\.
* The default <code>index\.rst</code> created by <code>antsibull\-docs sphinx\-init</code> includes the new environment variable index \([https\://github\.com/ansible\-community/antsibull\-docs/pull/80](https\://github\.com/ansible\-community/antsibull\-docs/pull/80)\)\.
* Use correct markup \(<code>envvar</code> role\) for environment variables\. Compile an index of all environment variables used by plugins \([https\://github\.com/ansible\-community/antsibull\-docs/pull/73](https\://github\.com/ansible\-community/antsibull\-docs/pull/73)\)\.

<a id="bugfixes-13"></a>
### Bugfixes

* Make sure that <code>build\.sh</code> created by the <code>sphinx\-init</code> subcommand sets proper permissions for antsibull\-docs on the <code>temp\-rst</code> directory it creates \([https\://github\.com/ansible\-community/antsibull\-docs/pull/79](https\://github\.com/ansible\-community/antsibull\-docs/pull/79)\)\.

<a id="v1-7-4"></a>
## v1\.7\.4

<a id="release-summary-17"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-14"></a>
### Bugfixes

* Removed <code>sphinx</code> restriction in <code>requirements\.txt</code> file created by <code>antsibull\-docs sphinx\-init</code> since the bug in <code>sphinx\-rtd\-theme</code> has been fixed \([https\://github\.com/ansible\-community/antsibull\-docs/pull/69](https\://github\.com/ansible\-community/antsibull\-docs/pull/69)\)\.
* The license header for the template for the <code>rst/index\.rst</code> file created by <code>antsibull\-docs sphinx\-init</code> was commented incorrectly and thus showed up in the templated file \([https\://github\.com/ansible\-community/antsibull\-docs/pull/67](https\://github\.com/ansible\-community/antsibull\-docs/pull/67)\)\.
* When using <code>\-\-squash\-hierarchy</code>\, do not mention the list of collections on the collection\'s index page \([https\://github\.com/ansible\-community/antsibull\-docs/pull/72](https\://github\.com/ansible\-community/antsibull\-docs/pull/72)\)\.

<a id="v1-7-3"></a>
## v1\.7\.3

<a id="release-summary-18"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-15"></a>
### Bugfixes

* Fix rendering of the <code>action\_group</code> attribute \([https\://github\.com/ansible\-community/antsibull\-docs/pull/62](https\://github\.com/ansible\-community/antsibull\-docs/pull/62)\)\.

<a id="v1-7-2"></a>
## v1\.7\.2

<a id="release-summary-19"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-16"></a>
### Bugfixes

* Fix <code>version\_added</code> processing for ansible\.builtin 0\.x to represent this as <code>Ansible 0\.x</code> instead of <code>ansible\-core 0\.x</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/61](https\://github\.com/ansible\-community/antsibull\-docs/pull/61)\)\.

<a id="v1-7-1"></a>
## v1\.7\.1

<a id="release-summary-20"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-17"></a>
### Bugfixes

* Prevent crash during <code>stable</code> docsite build when <code>\_python</code> entry is present in deps file \([https\://github\.com/ansible\-community/antsibull\-docs/pull/57](https\://github\.com/ansible\-community/antsibull\-docs/pull/57)\)\.

<a id="v1-7-0"></a>
## v1\.7\.0

<a id="release-summary-21"></a>
### Release Summary

Bugfix and feature release\.

<a id="minor-changes-13"></a>
### Minor Changes

* Add <code>\-\-intersphinx</code> option to the <code>sphinx\-init</code> subcommand to allow adding additional <code>intersphinx\_mapping</code> entries to <code>conf\.py</code> \([https\://github\.com/ansible\-community/antsibull\-docs/issues/35](https\://github\.com/ansible\-community/antsibull\-docs/issues/35)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/44](https\://github\.com/ansible\-community/antsibull\-docs/pull/44)\)\.
* Allow the <code>toctree</code> entries for in a collection\'s <code>docs/docsite/extra\-docs\.yml</code> to be a dictionary with <code>ref</code> and <code>title</code> keys instead of just a reference as a string \([https\://github\.com/ansible\-community/antsibull\-docs/pull/45](https\://github\.com/ansible\-community/antsibull\-docs/pull/45)\)\.
* Antsibull\-docs now depends on [packaging](https\://pypi\.org/project/packaging/) \([https\://github\.com/ansible\-community/antsibull\-docs/pull/49](https\://github\.com/ansible\-community/antsibull\-docs/pull/49)\)\.
* The collection index pages now contain the supported versions of ansible\-core of the collection in case collection\'s <code>meta/runtime\.yml</code> specifies <code>requires\_ansible</code> \([https\://github\.com/ansible\-community/antsibull\-docs/issues/48](https\://github\.com/ansible\-community/antsibull\-docs/issues/48)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/49](https\://github\.com/ansible\-community/antsibull\-docs/pull/49)\)\.
* The output of the <code>lint\-collection\-docs</code> command has been improved\; in particular multi\-line messages are now indented \([https\://github\.com/ansible\-community/antsibull\-docs/pull/52](https\://github\.com/ansible\-community/antsibull\-docs/pull/52)\)\.
* Use <code>ansible \-\-version</code> to figure out ansible\-core version when ansible\-core is not installed for the same Python interpreter / venv that is used for antsibull\-docs \([https\://github\.com/ansible\-community/antsibull\-docs/pull/50](https\://github\.com/ansible\-community/antsibull\-docs/pull/50)\)\.
* Use code formatting for all values\, such as choice entries\, defaults\, and samples \([https\://github\.com/ansible\-community/antsibull\-docs/issues/38](https\://github\.com/ansible\-community/antsibull\-docs/issues/38)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/42](https\://github\.com/ansible\-community/antsibull\-docs/pull/42)\)\.

<a id="bugfixes-18"></a>
### Bugfixes

* Avoid long aliases list to make left column too wide \([https\://github\.com/ansible\-collections/amazon\.aws/issues/1101](https\://github\.com/ansible\-collections/amazon\.aws/issues/1101)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/54](https\://github\.com/ansible\-community/antsibull\-docs/pull/54)\)\.
* Make <code>lint\-collection\-docs \-\-plugin\-docs</code> subcommand actually work \([https\://github\.com/ansible\-community/antsibull\-docs/pull/47](https\://github\.com/ansible\-community/antsibull\-docs/pull/47)\)\.

<a id="v1-6-1"></a>
## v1\.6\.1

<a id="release-summary-22"></a>
### Release Summary

Bugfix release for ansible\-core 2\.14\.

<a id="bugfixes-19"></a>
### Bugfixes

* Fix formulation of top\-level <code>version\_added</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/43](https\://github\.com/ansible\-community/antsibull\-docs/pull/43)\)\.

<a id="v1-6-0"></a>
## v1\.6\.0

<a id="release-summary-23"></a>
### Release Summary

Bugfix and feature release\.

<a id="minor-changes-14"></a>
### Minor Changes

* Allow to specify choices as dictionary instead of list \([https\://github\.com/ansible\-community/antsibull\-docs/pull/36](https\://github\.com/ansible\-community/antsibull\-docs/pull/36)\)\.
* Use JSON serializer to format choices \([https\://github\.com/ansible\-community/antsibull\-docs/pull/37](https\://github\.com/ansible\-community/antsibull\-docs/pull/37)\)\.
* Use special serializer to format INI values in examples \([https\://github\.com/ansible\-community/antsibull\-docs/pull/37](https\://github\.com/ansible\-community/antsibull\-docs/pull/37)\)\.

<a id="bugfixes-20"></a>
### Bugfixes

* Avoid collection names with <code>\_</code> in them appear wrongly escaped in the HTML output \([https\://github\.com/ansible\-community/antsibull\-docs/pull/41](https\://github\.com/ansible\-community/antsibull\-docs/pull/41)\)\.
* For INI examples which have no default\, write <code>VALUE</code> as intended instead of <code>None</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/37](https\://github\.com/ansible\-community/antsibull\-docs/pull/37)\)\.
* Format lists correctly for INI examples \([https\://github\.com/ansible\-community/antsibull\-docs/pull/37](https\://github\.com/ansible\-community/antsibull\-docs/pull/37)\)\.
* The <code>sphinx\-init</code> subcommand\'s <code>requirement\.txt</code> file avoids Sphinx 5\.2\.0\.post0\, which triggers a bug in sphinx\-rtd\-theme which happens to be the parent theme of the default theme sphinx\_ansible\_theme used by <code>sphinx\-init</code> \([https\://github\.com/ansible\-community/antsibull\-docs/issues/39](https\://github\.com/ansible\-community/antsibull\-docs/issues/39)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/40](https\://github\.com/ansible\-community/antsibull\-docs/pull/40)\)\.

<a id="v1-5-0"></a>
## v1\.5\.0

<a id="release-summary-24"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-15"></a>
### Minor Changes

* Detect filter and test plugin aliases and avoid them being emitted multiple times\. Instead insert redirects so that stub pages will be created \([https\://github\.com/ansible\-community/antsibull\-docs/pull/33](https\://github\.com/ansible\-community/antsibull\-docs/pull/33)\)\.
* Replace <code>ansible\.builtin</code> with <code>ansible\-core</code>\, <code>ansible\-base</code>\, or <code>Ansible</code> in version added collection names\. Also write <code>\<collection\_name\> \<version\></code> instead of <code>\<version\> of \<collection\_name\></code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/34](https\://github\.com/ansible\-community/antsibull\-docs/pull/34)\)\.

<a id="bugfixes-21"></a>
### Bugfixes

* Fix escaping of collection names in version added statements\, and fix collection names for roles options \([https\://github\.com/ansible\-community/antsibull\-docs/pull/34](https\://github\.com/ansible\-community/antsibull\-docs/pull/34)\)\.

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="release-summary-25"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-16"></a>
### Minor Changes

* The <code>sphinx\-init</code> subcommand now also creates an <code>antsibull\-docs\.cfg</code> file and moves configuration settings from CLI flags in <code>build\.sh</code> to this configuration file \([https\://github\.com/ansible\-community/antsibull\-docs/pull/26](https\://github\.com/ansible\-community/antsibull\-docs/pull/26)\)\.
* There are two new options for explicitly specified configuration files named <code>collection\_url</code> and <code>collection\_install</code>\. These allow to override the URLs pointing to collections \(default link to galaxy\.ansible\.com\)\, and the commands to install collections \(use <code>ansible\-galaxy collection install</code> by default\)\. This can be useful when documenting \(internal\) collections that are not available on Ansible Galaxy\. The default <code>antsibull\-docs\.cfg</code> generated by the <code>sphinx\-init</code> subcommand shows how this can be configured \([https\://github\.com/ansible\-community/antsibull\-docs/issues/15](https\://github\.com/ansible\-community/antsibull\-docs/issues/15)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/26](https\://github\.com/ansible\-community/antsibull\-docs/pull/26)\)\.
* When generating plugin error pages\, or showing non\-fatal errors in plugins or roles\, link to the collection\'s issue tracker instead of the collection\'s URL if available \([https\://github\.com/ansible\-community/antsibull\-docs/pull/29](https\://github\.com/ansible\-community/antsibull\-docs/pull/29)\)\.

<a id="bugfixes-22"></a>
### Bugfixes

* Make handling of bad documentation more robust when certain values are <code>None</code> while the keys are present \([https\://github\.com/ansible\-community/antsibull\-docs/pull/32](https\://github\.com/ansible\-community/antsibull\-docs/pull/32)\)\.

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="release-summary-26"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-17"></a>
### Minor Changes

* Ensure that values for <code>default</code>\, <code>choices</code>\, and <code>sample</code> use the types specified for the option / return value \([https\://github\.com/ansible\-community/antsibull\-docs/pull/19](https\://github\.com/ansible\-community/antsibull\-docs/pull/19)\)\.
* If a plugin or module has requirements listed\, add a disclaimer next to the installation line at the top that further requirements are needed \([https\://github\.com/ansible\-community/antsibull\-docs/issues/23](https\://github\.com/ansible\-community/antsibull\-docs/issues/23)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/24](https\://github\.com/ansible\-community/antsibull\-docs/pull/24)\)\.
* Show the \'you might already have this collection installed if you are using the <code>ansible</code> package\' disclaimer for plugins only for official docsite builds \(subcommands <code>devel</code> and <code>stable</code>\)\. Also include this disclaimer for roles on official docsite builds \([https\://github\.com/ansible\-community/antsibull\-docs/pull/25](https\://github\.com/ansible\-community/antsibull\-docs/pull/25)\)\.
* Use <code>true</code> and <code>false</code> for booleans instead of <code>yes</code> and <code>no</code> \([https\://github\.com/ansible\-community/community\-topics/issues/116](https\://github\.com/ansible\-community/community\-topics/issues/116)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/19](https\://github\.com/ansible\-community/antsibull\-docs/pull/19)\)\.
* When processing formatting directives\, make sure to properly escape all other text for RST respectively HTML instead of including it verbatim \([https\://github\.com/ansible\-community/antsibull\-docs/issues/21](https\://github\.com/ansible\-community/antsibull\-docs/issues/21)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/22](https\://github\.com/ansible\-community/antsibull\-docs/pull/22)\)\.

<a id="bugfixes-23"></a>
### Bugfixes

* Improve indentation of HTML blocks for tables to avoid edge cases which generate invalid RST \([https\://github\.com/ansible\-community/antsibull\-docs/pull/22](https\://github\.com/ansible\-community/antsibull\-docs/pull/22)\)\.

<a id="v1-2-2"></a>
## v1\.2\.2

<a id="release-summary-27"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-24"></a>
### Bugfixes

* Fix rstcheck\-core support \([https\://github\.com/ansible\-community/antsibull\-docs/pull/20](https\://github\.com/ansible\-community/antsibull\-docs/pull/20)\)\.

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="release-summary-28"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-25"></a>
### Bugfixes

* Do not escape <code>\<</code>\, <code>\></code>\, <code>\&</code>\, and <code>\'</code> in JSONified defaults and examples as the [Jinja2 tojson filter](https\://jinja\.palletsprojects\.com/en/2\.11\.x/templates/\#tojson) does\. Also improve formatting by making sure <code>\,</code> is followed by a space \([https\://github\.com/ansible\-community/antsibull\-docs/pull/18](https\://github\.com/ansible\-community/antsibull\-docs/pull/18)\)\.
* The collection filter was ignored when parsing the <code>ansible\-galaxy collection list</code> output for the docs build \([https\://github\.com/ansible\-community/antsibull\-docs/issues/16](https\://github\.com/ansible\-community/antsibull\-docs/issues/16)\, [https\://github\.com/ansible\-community/antsibull\-docs/pull/17](https\://github\.com/ansible\-community/antsibull\-docs/pull/17)\)\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary-29"></a>
### Release Summary

Feature and bugfix release\.

<a id="minor-changes-18"></a>
### Minor Changes

* Support plugin <code>seealso</code> from the [semantic markup specification](https\://hackmd\.io/VjN60QSoRSSeRfvGmOH1lQ\?both) \([https\://github\.com/ansible\-community/antsibull\-docs/pull/8](https\://github\.com/ansible\-community/antsibull\-docs/pull/8)\)\.
* The <code>lint\-collection\-docs</code> subcommand has a new boolean flag <code>\-\-plugin\-docs</code> which renders the plugin docs to RST and validates them with rstcheck\. This can be used as a lighter version of rendering the docsite in CI \([https\://github\.com/ansible\-community/antsibull\-docs/pull/12](https\://github\.com/ansible\-community/antsibull\-docs/pull/12)\)\.
* The files in the source repository now follow the [REUSE Specification](https\://reuse\.software/spec/)\. The only exceptions are changelog fragments in <code>changelogs/fragments/</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/14](https\://github\.com/ansible\-community/antsibull\-docs/pull/14)\)\.

<a id="bugfixes-26"></a>
### Bugfixes

* Make sure that <code>\_input</code> does not show up twice for test or filter arguments when the plugin mentions it in <code>positional</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/10](https\://github\.com/ansible\-community/antsibull\-docs/pull/10)\)\.
* Mark rstcheck 4\.x and 5\.x as compatible\. Support rstcheck 6\.x as well \([https\://github\.com/ansible\-community/antsibull\-docs/pull/13](https\://github\.com/ansible\-community/antsibull\-docs/pull/13)\)\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-30"></a>
### Release Summary

Feature release with support for ansible\-core 2\.14\'s sidecar docs feature\.

<a id="minor-changes-19"></a>
### Minor Changes

* If lookup plugins have a single return value starting with <code>\_</code>\, that return value is now labelled <code>Return value</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/6](https\://github\.com/ansible\-community/antsibull\-docs/pull/6)\)\.
* If lookup plugins have an option called <code>\_terms</code>\, it is now shown in its own section <code>Terms</code>\, and not in the regular <code>Parameters</code> section \([https\://github\.com/ansible\-community/antsibull\-docs/pull/6](https\://github\.com/ansible\-community/antsibull\-docs/pull/6)\)\.
* More robust handling of parsing errors when ansible\-doc was unable to extract documentation \([https\://github\.com/ansible\-community/antsibull\-docs/pull/6](https\://github\.com/ansible\-community/antsibull\-docs/pull/6)\)\.
* Support parameter type <code>any</code>\, and show <code>raw</code> as <code>any</code> \([https\://github\.com/ansible\-community/antsibull\-docs/pull/6](https\://github\.com/ansible\-community/antsibull\-docs/pull/6)\)\.
* Support test and filter plugins when ansible\-core 2\.14\+ is used\. This works with the current <code>devel</code> branch of ansible\-core \([https\://github\.com/ansible\-community/antsibull\-docs/pull/6](https\://github\.com/ansible\-community/antsibull\-docs/pull/6)\)\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="release-summary-31"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes-27"></a>
### Bugfixes

* Make sure that aliases of module/plugin options and return values that result in identical RST labels under docutil\'s normalization are only emitted once \([https\://github\.com/ansible\-community/antsibull\-docs/pull/7](https\://github\.com/ansible\-community/antsibull\-docs/pull/7)\)\.
* Properly escape module/plugin option and return value slugs in generated HTML \([https\://github\.com/ansible\-community/antsibull\-docs/pull/7](https\://github\.com/ansible\-community/antsibull\-docs/pull/7)\)\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-32"></a>
### Release Summary

First stable release\.

<a id="major-changes-2"></a>
### Major Changes

* From version 1\.0\.0 on\, antsibull\-docs is sticking to semantic versioning and aims at providing no backwards compatibility breaking changes <strong>to the command line API \(antsibull\-docs\)</strong> during a major release cycle\. We explicitly exclude code compatibility\. <strong>antsibull\-docs is not supposed to be used as a library\,</strong> and when used as a library it might not conform to semantic versioning \([https\://github\.com/ansible\-community/antsibull\-docs/pull/2](https\://github\.com/ansible\-community/antsibull\-docs/pull/2)\)\.

<a id="minor-changes-20"></a>
### Minor Changes

* Only mention \'These are the collections with docs hosted on docs\.ansible\.com\' for <code>stable</code> and <code>devel</code> subcommands \([https\://github\.com/ansible\-community/antsibull\-docs/pull/3](https\://github\.com/ansible\-community/antsibull\-docs/pull/3)\)\.
* Stop using some API from antsibull\-core that is being removed \([https\://github\.com/ansible\-community/antsibull\-docs/pull/1](https\://github\.com/ansible\-community/antsibull\-docs/pull/1)\)\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-33"></a>
### Release Summary

Initial release\. The <code>antsibull\-docs</code> tool is compatible to the one from antsibull 0\.43\.0\.
