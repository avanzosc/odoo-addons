.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

=========================================
Product Template Default Service Tracking
=========================================

Overview
========

The **Product Template Default Service Tracking** module modifies the behavior of the **`service_tracking`** field in the **`product.template`** model. It ensures that the **`service_tracking`** field is automatically set to **`project_only`** if no value is provided during the creation of a product template.

Features
========

- Automatically sets the **`service_tracking`** field to **`project_only`** when a new product template is created and no value for this field is provided.
- This behavior applies to all product templates of type **Service**, where the **`service_tracking`** field controls the tracking mechanism for services.

Usage
=====

1. Create a new product template.
2. If no value is set for the **`service_tracking`** field, it will default to **`project_only`**.
3. This ensures that all new service products are tracked based on the project settings without requiring manual configuration.

Configuration
=============

No additional configuration is required.

Testing
=======

1. Create a **Product Template** for a service.
2. Ensure that the **`service_tracking`** field is automatically set to **`project_only`** if no value is provided.

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
