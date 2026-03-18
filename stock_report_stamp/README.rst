.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

======================
stock_report_stamp
======================

Overview
========

The **stock_report_stamp** module extends the **stock** module by including the company’s digital signature and stamp images on delivery documents. This enhancement provides a more professional and personalized touch to the reports.

Features
========

- Displays the company's digital signature image on delivery documents if configured in the **Company** settings.

- Displays the company's stamp image on delivery documents if configured in the **Company** settings.

Usage
=====

1. **Install the Module**:

   - Install the **stock_report_stamp** module via the Apps menu.

2. **Configure Signature and Stamp**:

   - Ensure the **res_company_signature_fields** module is installed and populate the **Signature Image** and **Stamp Image** fields in the **Company** settings.

3. **View Delivery Documents**:

   - Generate or print a delivery document. The report will display the company's digital signature and stamp if they are configured.

Configuration
=============

This module depends on the **res_company_signature_fields** module, which provides the fields for storing the signature and stamp images.

Testing
=======

Test the following scenarios to ensure the module functions as expected:

- **Test Signature Display**:

  - Generate a delivery document with a configured signature image in the **Company** settings. Verify that the image appears on the document.

- **Test Stamp Display**:

  - Generate a delivery document with a configured stamp image in the **Company** settings. Check that the image is displayed as expected.

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
