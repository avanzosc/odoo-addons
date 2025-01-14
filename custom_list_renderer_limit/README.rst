.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

==========================
Custom List Renderer Limit
==========================

Overview
========

The **Custom List Renderer Limit** module extends the **ListRenderer** functionality in Odoo's backend by introducing a limit on the number of records displayed in list views. By default, the limit is set to 100 records, improving performance for users with large datasets.

Features
========

- **Rendering Limit**:

  - Adds a limit on the number of records rendered in the list views in the Odoo backend.

  - Default limit is set to 100 records.

Usage
=====

1. **Install the Module**:
   - Install the **Custom List Renderer Limit** module via the Apps menu.

2. **Observe the Changes**:
   - Navigate to any list view in the Odoo backend.
   - The list will display a limited number of records based on the limit set in the module (default: 100).

3. **Customize the Limit**:
   - If you wish to change the number of records displayed, update the `limit` value in the JavaScript file (`static/src/js/list_renderer.js`) of the module.

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
