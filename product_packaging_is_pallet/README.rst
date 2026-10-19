.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=============================
Product Packaging Is Pallet
=============================

Summary
-------
This module extends the **product.packaging** model by adding a boolean field
**Is Pallet** to quickly mark whether a packaging is a pallet. It also
hides the standard ``package_type_id`` field in the form and tree views to keep
the UI focused.

Key Features
------------
- New checkbox **Is Pallet** on product packaging.
- Visible in both **form** and **tree** views.
- Hides ``package_type_id`` in those views.

Installation
------------
1. Copy the module directory into your Odoo ``addons`` path (e.g. ``/odoo/custom/addons``).
2. Update the Apps list and install the module from **Apps**.
   Alternatively, from the command line you can update the module:
   ::
     
     ./odoo-bin -d <your_db> -u <module_name>

Dependencies
------------
- stock

Configuration & Usage
---------------------
1. Go to **Settings → Inventory → Products** and enable **Product Packaging** checkbox 
2. Go to **Inventory → Configuration → Products Packagings** (or open a Product
   and navigate to its **Packaging**).
3. Create or edit a packaging and enable the **Is Pallet** checkbox when the
   packaging corresponds to a pallet.
4. The standard **Package Type** field is hidden by this module in form and list
   views.

Technical Notes
---------------
- Model inheritance: ``product.packaging`` adds ``is_pallet = fields.Boolean(default=False)``.
- View customizations:
  - Adds ``is_pallet`` after ``product_id`` in the form view.
  - Adds ``is_pallet`` (optional column) after ``name`` in the tree view.
  - Sets ``package_type_id`` as invisible in both views.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>

* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.

