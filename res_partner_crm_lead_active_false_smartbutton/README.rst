.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=============================================
Res Partner CRM Lead Active False Smartbutton
=============================================

Overview
========

The **Res Partner CRM Lead Active False Smartbutton** module adds a smart button to the customer form view to easily access inactive CRM leads (leads marked as inactive) related to that customer.

Features
========

- **Smart Button for Inactive Leads**:
  
  - Adds a smart button labeled "Inactive Leads" on the customer form.
  - The button is only visible when there are inactive leads associated with the customer.
  - Clicking the button opens a filtered view of inactive leads related to the customer.

Usage
=====

1. **Install the Module**:
   
   - Install the module via Odoo's Apps interface.

2. **View Inactive Leads**:

   - Navigate to the customer form in Contacts.
   - If the customer has inactive leads, the "Inactive Leads" button will appear.
   - Click on the button to view and manage the inactive leads for that customer.

Configuration
=============

No additional configuration is required. The module is ready to use upon installation.

Testing
=======

Test the following scenarios:

- **Inactive Leads Access**:
  
  - Verify that clicking the button opens the list view of inactive leads filtered by the current customer.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
