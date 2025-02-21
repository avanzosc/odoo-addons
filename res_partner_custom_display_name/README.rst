.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===============================
Res Partner Custom Display Name
===============================

Overview
========

The **Res Partner Custom Display Name** module allows users to define a custom display name for contacts (`res.partner`).  
If a custom display name is set, it will be used instead of the default Odoo-generated display name.

Features
========

- Adds a new **custom_display_name** field to the `res.partner` model.
- Custom display name can be set manually by the user.
- If the field is filled, it replaces the default computed display name.
- The custom display name appears in:
  - **Contact Form View**
  - **Contact Tree View**

Usage
=====

1. **Install the Module**:
   - Install the **Res Partner Custom Display Name** module from the Apps menu.

2. **Set a Custom Display Name**:
   - Navigate to *Contacts* → *Contacts*.
   - Open any contact record.
   - Enter a value in the new field **Custom Display Name**.
   - Save the record.

3. **View the Custom Display Name**:
   - The tree view will now display the **Custom Display Name** instead of the default computed name.

Configuration
=============

No additional configuration is required. The field will be automatically available after module installation.

Testing
=======

1. Go to *Contacts* → *Contacts*.
2. Open or create a contact.
3. Set a **Custom Display Name** and save.
4. Verify that the display name updates accordingly.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/sale-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
