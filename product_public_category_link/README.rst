.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

============================
Product Public Category Link
============================

This module extends the **Product Category** and **Product Template** models to provide synchronization between internal product categories and public e-commerce categories.

**Features**

- **Bidirectional Sync**: Automatically synchronizes public categories when internal categories change
- **Manual Control**: Remove public categories from products using a dedicated wizard
- **UI Integration**: Adds public category field to product categories with tag widget
- **Bulk Operations**: Efficient handling of multiple products and categories

**Main Functionality**

- **Automatic Sync**: When adding public categories to a product category, all products in that category are automatically updated
- **Selective Removal**: Use the "Remove Public Categories" button to clean public categories from products while maintaining control
- **On-change Support**: Real-time synchronization when changing product categories in the UI

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