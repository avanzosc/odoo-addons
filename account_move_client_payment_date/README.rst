.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

================================
Account Move Client Payment Date
================================

Overview
========

The **Account Move Client Payment Date** module adds a new field to account moves to track the date when the client is expected to make the payment. This feature allows for better management and tracking of payment expectations directly within the account move records.

Features
========

- **Client Payment Date Field**:

  - Adds a `client_payment_date` field to account moves, enabling users to record and track the expected payment date from clients.

- **Form View Modification**:

  - Includes the `client_payment_date` field in the account move form view under the extra information tab.

- **Tree View Modification**:

  - Displays the `client_payment_date` field in the account move tree view for easy visibility.

- **Search View Modification**:

  - Adds the `client_payment_date` field to the search filters and grouping options.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Access Account Moves**:

   - Navigate to **Accounting** and open the **Account Moves** menu.

3. **View and Edit Payment Date**:

   - Open any account move record and you will find the **Client Payment Date** field in the form view. You can also view it in the list view and use it as a search filter.

Configuration
=============

- **User Permissions**:

  - Ensure that the user has the necessary permissions to view and edit the new field in account move records.

Testing
=======

Test the following scenarios:

- **Field Visibility**:

  - Verify that the `client_payment_date` field is correctly displayed in the form view, tree view, and search view.

- **Field Functionality**:

  - Check that the field is functional and allows for correct date entry and retrieval.

- **Search and Filter**:

  - Ensure that the `client_payment_date` field can be used effectively in search and filtering operations.

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
