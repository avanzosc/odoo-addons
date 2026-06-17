.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===============================================================
Crossovered Budget Lines Hide Theoretical Amount and Percentage
===============================================================


Overview
========

The **Crossovered Budget Lines Hide Theoretical Amount and Percentage** module customizes the `crossovered.budget.lines` view by hiding the theoretical amount and percentage columns. This is useful for streamlining the budget lines view by removing unnecessary information.

Features
========

- **Tree View Modification**:

  - Hides the `theoretical_amount` and `percentage` columns from the `crossovered.budget.lines` tree view.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Access Budget Lines**:

   - Navigate to **Accounting** > **Crossovered Budget Lines**.

3. **View Customization**:

   - The `theoretical_amount` and `percentage` columns will no longer be visible in the tree view of crossovered budget lines.

Configuration
=============

- **User Permissions**:

  - Ensure that users have the necessary permissions to view the modified tree view.

Testing
=======

Test the following scenarios:

- **Column Visibility**:

  - Verify that the `theoretical_amount` and `percentage` columns are hidden in the tree view.

- **View Integrity**:

  - Ensure that other functionalities and views related to `crossovered.budget.lines` remain unaffected.

Bug Tracker
===========

For bugs and issues, please visit `GitHub Issues <https://github.com/avanzosc/account-addons/issues>`_ to report or track issues.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>

* Ana Juaristi <anajuaristi@avanzosc.es>

Please contact contributors for module-specific questions, but direct support requests should be made through the official channels.

License
=======
This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
