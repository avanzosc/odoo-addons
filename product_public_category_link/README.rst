.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

============================
Product Public Category Link
============================

This module links internal **Product Categories** with **Website (public) Categories**, so that products automatically pick up the website categories configured on their internal category.

**Features**

- **Configuration**: Adds a "Public Category" field to the product category form, to define which website categories correspond to it
- **Additive Sync**: When a product's internal category is set or changed in the form, its missing website categories are added automatically — existing ones are never removed
- **Manual Removal**: A button on the product category form removes its public categories, and those of its products, after confirmation

**Main Functionality**

- **On-change Support**: Changing the "Product Category" field on a product suggests its configured website categories, adding only the ones the product doesn't already have
- **Selective Removal**: Use the "Remove Public Categories" button on the product category to clear the public categories from that category and from all products currently assigned to it

Note: editing the "Public Category" field on the product category itself does **not** retroactively update products that were already linked to it — the sync only happens when the product's own category is set/changed on the product form.

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
* Aner Arregi <anerarregi@avanzosc.es>


For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.