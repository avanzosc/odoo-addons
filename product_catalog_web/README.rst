.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================
Product Catalog Web
===================

This module allows you to create and manage product catalogs intended for web or
e-commerce use. Each catalog groups a set of products and stores configuration
such as logo, description, inventory availability policy, warehouse, and whether
it should be visible as a slider on the website.

Products can be added to a catalog manually or by importing an Excel file that
lists products by their internal reference. The module also adds a **Catalogs**
field on each product template so you can see at a glance which catalogs a
product belongs to.

Key features:

* Create named catalogs with logo, description, and per-warehouse stock settings.
* Assign products to one or more catalogs via a many-to-many relation.
* **Import** products into a catalog from an ``.xlsx`` file (matched by internal
  reference). An option lets you replace the existing product list entirely.
* **Export** the current product list of a catalog to an ``.xlsx`` file
  (internal reference + name).
* **Website page** at ``/shop/catalog`` listing all active catalogs that have
  *Visible on Website* enabled, with logo and name. Supports name search.

Usage / How to test
===================

Backend
-------

1. Go to **Sales → Products → Web Catalogs**.
2. Create a new catalog, fill in the name, warehouse, and inventory availability,
   and save.
3. Open the catalog form. In the **Products** tab, add products manually or use
   the **Import products** button to upload an ``.xlsx`` file where column A
   contains internal references (the first row is treated as a header and is
   skipped).
4. Use **Export products** to download the product list as an Excel file and
   verify the contents.
5. On any product template (*Sales → Products → Products*), check the
   **Catalogs** field to confirm the relation is reflected on the product side.

Website
-------

6. Make sure the **Visible on Website** checkbox is enabled on at least one
   catalog.
7. Navigate to ``/shop/catalog`` — the catalog page should display the active
   and visible catalogs as cards with their logo and name.
8. Use the search box to filter catalogs by name.

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
