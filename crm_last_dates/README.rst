.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

========================================================
CRM Last Dates
========================================================

Overview
========

The **CRM Last Dates** module adds the last lead, meeting, and invoice dates to the `res.partner` model. This enhancement provides valuable information for sales and account management by allowing users to easily track the most recent interactions and transactions with partners.

Features
========

- **Last Lead Date**: Displays the date of the last lead associated with the partner.
- **Last Meeting Date**: Shows the date of the most recent meeting related to the partner.
- **Last Invoice Date**: Indicates the date of the latest invoice issued to the partner.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Access Partner Records**:

   - Navigate to **Contacts** > **Partners**.

3. **View Last Dates**:

   - Open any partner record to view the new fields under the **Sales & Purchases** tab.

Configuration
=============

- **User Permissions**:

  - Ensure that users have the necessary permissions to view partner records and related information.

Testing
=======

Test the following scenarios:

- **Field Visibility**:

  - Verify that the `Last Lead Date`, `Last Meeting Date`, and `Last Invoice Date` fields are correctly displayed in the partner form view.

- **Data Accuracy**:

  - Ensure that the dates reflect the correct last lead, meeting, and invoice information for various partners.

Bug Tracker
===========

For bugs and issues, please visit `GitHub Issues <https://github.com/avanzosc/crm-addons/issues>`_ to report or track issues.

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
