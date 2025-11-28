.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

================================
MRP Package Procurement Sequence
================================

This module extends **MRP Production** and **Stock Move Lines** to improve package creation and tracking of finished products. It introduces logic to count and display packaged finished moves linked to a procurement group, ensuring sequential package naming and better visibility in manufacturing workflows.

Key Features
============

- Adds a computed field `packaged_finished_moves` to procurement groups and productions.
- Automatically generates sequential package names based on procurement group identifiers.
- Provides a smart button in the production form to quickly access packaged finished move lines.
- Enhances traceability of finished products by linking them to created packages.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



