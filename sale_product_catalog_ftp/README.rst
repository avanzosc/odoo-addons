.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

========================
Product Catalog FTP Sync
========================

This module generates a per-customer xlsx stock export from a
``product.catalog`` (see ``sale_product_catalog``) and uploads it to the
customer's own FTP server on a daily schedule.

For each customer/catalog combination, an FTP configuration record stores
the destination server, credentials, and target folder. A daily cron job
(re)generates the catalog's xlsx file and uploads it via FTP, replacing any
previous export. Product, EAN code, reference, brand, category, price, RRP
and B2B stock (see ``stock_b2b_availability``) are exported as fixed
columns, followed by one column per product attribute found in the catalog.

Key features
============

* **FTP export configuration** per catalog/customer: server, user, password
  and destination folder, with an error field showing the last FTP failure
  (if any).
* Daily **scheduled action** that regenerates and re-uploads every active
  configuration.
* xlsx report (via ``report_xlsx``) with a fixed set of columns (product,
  EAN, reference, brand, category, price validity dates, price, RRP, B2B
  stock) plus one column per product attribute present in the catalog.
* RRP column uses the pricelist item's RRP (``pvp_price``, from
  ``product_pricelist_import_spf``) when a matching pricelist rule is found
  for the customer, falling back to the product's price with taxes
  otherwise.
* Deactivating a configuration, or reassigning its catalog/customer, clears
  the locally cached file and removes the file from the FTP server.

Migration from v12
===================

On a database migrated from v12 (``website_portal_catalog`` /
``product.catalog.ftp``), the ``product_catalog_ftp`` table is carried over
as-is (same columns, same rows) with ``catalog_id`` pointing at what is now
``product.catalog`` (see ``sale_product_catalog``'s own migration). This
module's ``pre_init_hook`` removes only the rows whose ``catalog_id`` has no
matching ``product.catalog`` record, since installing the module adds a
foreign key on that column and a single orphaned row would make the
``ADD CONSTRAINT`` fail and abort the install. No other row is touched.

Usage / How to test
====================

1. Go to **Sales → Products → Catalogs → Upload Catalog to FTP**.
2. Create a record: pick the catalog and the customer, and fill in the FTP
   server, user, password and folder.
3. Run the **Create / Upload catalog to FTPs** scheduled action manually (or
   wait for its daily run) and check the **ftp_error** field is empty.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
