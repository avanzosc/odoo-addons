.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

==========================================
Product Template Onchange Service Tracking
==========================================

Overview
========

The **Product Template Onchange Service Tracking** module modifies the behavior of the **`service_tracking`** field in the **`product.template`** model. It ensures that when the field is set to **`no`**, it automatically changes to **`project_only`**.

Features
========

- Automatically updates the **`service_tracking`** field to **`project_only`** when it is initially set to **`no`**.
- Ensures consistency in the tracking mechanism for service products.
- Works seamlessly with the existing Odoo `onchange` mechanism.

Usage
=====

1. Modify the **`service_tracking`** field of a **Service** product template.
2. If it is set to **`no`**, the system will automatically change it to **`project_only`**.
3. The change happens dynamically when editing the record.

Configuration
=============

No additional configuration is required.

Testing
=======

1. Open a **Product Template** of type **Service**.
2. Set the **`service_tracking`** field to **`no`**.
3. Verify that the field automatically updates to **`project_only`**.

Bug Tracker
===========

Bugs and issues can be reported on the GitHub repository:
`GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For further information, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License.
For more details, see the LICENSE file or visit:
<https://www.gnu.org/licenses/lgpl-3.0.html>.
