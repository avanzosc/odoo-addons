.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=================================
Quality Control Tests Name Unique
=================================

This module ensures that quality control test names are unique, preventing duplicate names and improving test identification.

Features
--------

Unique Test Names: Enforces a database-level constraint to prevent quality control tests from sharing the same name.

Automatic Naming on Duplication: When duplicating a quality control test, automatically generates a unique name by appending (copy 2), (copy 3), etc., if necessary.
Clear Error Messages: Displays a validation error when attempting to create or rename a test with an existing name.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
~~~~~~~~~~~~

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente<alfredodelafuente@avanzosc.es>

