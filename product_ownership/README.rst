.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

=================
Product Ownership
=================

Overview
========

The **Product Ownership** module adds a Many2many field to `product.template` that allows linking up to three company partners as owners of a product. This helps in tracking product ownership within an organization.

Features
========

- Adds a **Client Owners** field to the product form.

- Allows selecting up to **three** company partners as owners.

- Enforces a constraint to prevent selecting more than three owners.

- Adds the **Client Owners** field to the product form and tree views.

- Ensures only companies can be selected as product owners.

Usage
=====

1. Navigate to **Inventory → Products**.

2. Open any product template.

3. In the **Ownership** section, select up to three company partners as owners.

4. The owners will be displayed in both the form and tree views.

Configuration
=============

No additional configuration is required.

Testing
=======

1. Assign **more than three owners** to a product and verify that an error is raised.

2. Check that only **company partners** can be selected.

3. Ensure that the **Client Owners** field appears in both the product form and tree views.

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
