.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

========================
purchase_report_stamp
========================

Overview
========

The **purchase_report_stamp** module extends the **purchase** module by adding the company’s digital signature and stamp images to purchase order reports. This functionality enhances the presentation and authenticity of purchase documents.

Features
========

- Displays the company's digital signature image on purchase orders if configured in the **Company** settings.

- Displays the company's stamp image on purchase orders if configured in the **Company** settings.

Usage
=====

1. **Install the Module**:

   - Install the **purchase_report_stamp** module via the Apps menu.

2. **Configure Signature and Stamp**:

   - Ensure the **res_company_signature_fields** module is installed and populate the **Signature Image** and **Stamp Image** fields in the **Company** settings.

3. **View Purchase Orders**:

   - Generate or print a purchase order. The report will display the company's digital signature and stamp if they are configured.

Configuration
=============

This module depends on the **res_company_signature_fields** module, which provides the fields for storing the signature and stamp images.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Signature Display**:

  - Generate a purchase order with a configured signature image in the **Company** settings. Verify that the image appears on the document.

- **Test Stamp Display**:

  - Generate a purchase order with a configured stamp image in the **Company** settings. Check that the image is displayed as expected.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
