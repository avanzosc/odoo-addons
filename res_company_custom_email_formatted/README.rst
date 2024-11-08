.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===========================================
Res Company Custom Email Formatted
===========================================

Overview
========

The **Res Company Custom Email Formatted** module extends the `res.company` model to customize the email formatting behavior for companies. It introduces a field for selecting a default email formatted company, allowing businesses to control how email addresses are formatted for their companies.

Features
========

- **Default Email Formatted Company**: Adds a field to the `res.company` form to allow users to select a company that will be used for the default email formatting.
  
- **Email Formatting Customization**: When a default email formatted company is selected, its email formatting will be applied to the current company.

Usage
=====

1. **Install the Module**:

   - Install the **Res Company Custom Email Formatted** module through the Apps menu.

2. **Configure Email Formatting**:

   - Go to the **Company** form view.

   - Under the **Settings** tab, select a company as the **Default Email Formatted**.

3. **Automatic Email Formatting**:

   - The selected default email formatted company will automatically apply its email formatting to the current company.

Configuration
=============

No additional configuration is required. Simply select a default email formatted company in the company settings.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Default Email Formatting**:

  - Create a new company and set a default email formatted company. Ensure the email formatting is applied accordingly.

- **Test Email Formatting with Different Companies**:

  - Try changing the default email formatted company and verify the changes are reflected.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
