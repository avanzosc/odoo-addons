.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Stock Lock Lot
==============

Overview
========

The **Stock Lock Lot** module enhances Odoo's stock management by adding a stage concept to stock lots. This stage can be used to block certain lots from being selected during stock operations, such as stock moves and manual assignments. This module helps to enforce inventory rules and manage stock availability more effectively.

Features
========

- **Stock Lot Stage**:

  - Introduces a new model `stock.lot.stage` to manage stages for stock lots.

  - Allows marking a stage as "blocking", which prevents lots in that stage from being selected.

- **Enhanced Stock Move Lines**:

  - Modifies the stock move line form to filter out lots in blocking stages.

- **Manual Stock Assignment**:

  - Updates the manual stock assignment view to exclude lots from blocking stages.

- **Stock Lot Views**:

  - Adds a field to the stock lot form to display the current stage.

Usage
=====

After installing the module, the following changes will be applied:

- **Stock Lots**:

  - A new "Stage" field will be available on the stock lot form. This allows you to assign a stage to each lot.

- **Stock Move Lines**:

  - The lot selection field will exclude lots that are in stages marked as blocking.

- **Manual Stock Assignment**:

  - The lot selection in manual stock assignments will also exclude lots in blocking stages.

Configuration
=============

1. **Define Stages**:

   - Go to `Inventory > Configuration > Stock Lot Stages` and create stages with the "Stage Blocking" checkbox enabled to block lots in those stages.

2. **Update Existing Lots**:

   - Ensure that existing lots are updated with appropriate stages as required.

Testing
=======

The module has been designed with the following functionalities in mind:

- **Creation and Assignment of Stock Lot Stages**:

  - Test the creation of stock lot stages and verify that lots in blocking stages are properly excluded from selection.

- **Integration with Stock Move Lines and Manual Assignments**:

  - Test stock moves and manual stock assignments to ensure lots in blocking stages are excluded as expected.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/project-addons/issues>`_. Please check there for existing issues or to report new ones.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>

* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.

License
=======

This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <http://www.gnu.org/licenses/agpl-3.0-standalone.html>.
