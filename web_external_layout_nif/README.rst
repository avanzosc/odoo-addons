.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

============================
Web External Layout NIF
============================

Overview
========

The **Web External Layout NIF** module customizes the standard external layout templates in Odoo to include the `NIF` (VAT) field for partner records. This field is conditionally displayed in the header section of documents if the partner's `VAT` (NIF) is available.

Features
========

- **NIF Field in External Layouts**:
  
  - Adds a `NIF` field (VAT) to multiple external layout templates:
    - `web.external_layout_standard`
    - `web.external_layout_bold`
    - `web.external_layout_striped`
    - `web.external_layout_boxed`
  - The `NIF` field is shown only if the partner's VAT information is available.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Generate Documents with NIF Field**:

   - When printing documents that use any of the customized layouts, the `NIF` field will appear in the document header if the partner has a VAT number.

Configuration
=============

No additional configuration is needed. The module automatically applies the change to the specified layouts.

Testing
=======

Test the following scenarios:

- **Document Printing**:
  
  - Print documents using the supported layouts and verify that the `NIF` field appears in the header section for partners with a VAT number.
  - For partners without a VAT number, confirm that the `NIF` field does not appear.

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
