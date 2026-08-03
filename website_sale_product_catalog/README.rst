.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==============================
Website Sale Product Catalog
==============================

This module extends ``sale_product_catalog`` to integrate product catalogs into
the website. It adds a **Visible on Website** flag to catalogs, a dedicated
catalog browsing section, and a configurable catalog filter on the ``/shop``
page.

Key features
============

* **Visible on Website** flag per catalog — only flagged catalogs belonging to
  the current company appear on the website.
* Translatable catalog names and descriptions for multilingual websites.
* **Catalogs page** (``/catalogs``) — searchable catalog cards (logo + name)
  accessible from the main navigation menu, with customer-facing grid/list
  layout buttons.
* **Catalog detail page** (``/catalog/<id>``) — shows the catalog products that
  have a currently valid item in the customer's pricelist, with variant names,
  prices, public-category and attribute filters.
* **Catalog detail toolbar** with optional product search, sorting, and
  customer-facing grid/list layout buttons. The selected layout is stored in
  the visitor session.
* **Catalog detail customization** from the website editor: columns, spacing,
  card style, image ratio and fill mode, product descriptions, search, sorting,
  layout buttons, cart buttons, and independent left/top placement for price,
  category, and attribute filters.
* **Per-product card customization** reusing Odoo's native eCommerce editor:
  card size, featured ordering, and product ribbons.
* **Cart redirect** — adding a product to the cart from a catalog detail page
  redirects the customer back to that catalog page instead of the shop cart.
* **Catalog breadcrumb on product detail** — when a visitor navigates from a
  catalog to a product page (``/shop/product/<slug>?catalog_id=<id>``), the
  breadcrumb replaces "All Products" with a back-link to that catalog.
* **Catalog filter on /shop** — customers can filter the product grid by one
  catalog at a time; leaving the filter empty shows all products.
* **Two filter layout modes**, toggled from the website editor panel:

  * **Left** — dropdown in the left sidebar, alongside existing category and
    attribute filters. The sidebar is automatically shown even when no category
    or attribute filters are active.
  * **Top** — pill filmstrip above the product grid, in the same style as
    Odoo's built-in category filmstrip.

* Filter layout modes are independent: both, one, or neither can be active at
  the same time.
* The shop filter persists across pagination and other URL parameters
  (``catalog_ids`` is preserved by ``keep()``).
* **Migration hook** — on first install, ``post_init_hook`` copies
  ``visible_slider`` values from the legacy ``product_catalog_web`` table if
  upgrading from a prior version of this module.

Usage / How to test
===================

1. Install ``sale_product_catalog`` and ``website_sale_product_catalog``.
2. Go to **Sales → Products → Catalogs** and enable **Visible on Website** on
   at least one catalog.
3. Navigate to ``/catalogs`` on the website — the catalog grid should appear
   with logo and name for each visible catalog. Use the search bar to filter
   catalogs by name or description.
4. Click a catalog card to open ``/catalog/<id>`` and browse its products.
5. Open the website editor on a catalog detail page and use **Customize →
   Catalog** to configure columns, toolbar options, cards, and filters.
6. Add a product to the cart from the catalog detail page — confirm the
   redirect lands back on the same catalog page.
7. Click a product name or image to open its detail page — the breadcrumb
   should show the catalog name and link back to ``/catalog/<id>``.
8. Open the website editor on the shop page (``/shop``), go to
   **Customize → Catalog Filter** and activate **Left**, **Top**, or both.
9. Exit the editor and go to the shop — the catalog filter should be visible.
10. Select a catalog pill or choose one from the dropdown to filter products;
    clear the selection to show all products again.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical
issues.

Credits
=======

Contributors
------------

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
