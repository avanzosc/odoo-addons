.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

========================
Product Product Category
========================

Overview
========

The **Product Product Category** module adds a new field for the product category on the product variant form. This field is automatically populated based on the product template category and is made visible in both the form view and tree view of the product variants.

Features
========

- **Product Category on Product Variant**:
  
  - A new field called `product_category` is added to the `product.product` model.
  - The product category is automatically populated based on the `product_tmpl_id.categ_id` (category of the product template).
  - The field is visible in both the product form view and the product tree view for product variants.

- **Post Installation Hook**:
  
  - The module includes a post-initialization hook to automatically update the `product_category` field on all existing products based on their product template.

Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **View Product Category on Product Variant**:

   - Go to the product form view. You will see a new `Product Category` field that reflects the category of the corresponding product template.
   - In the product tree view, the `Product Category` field will also be displayed.

Configuration
=============

No additional configuration is required. The module will automatically populate the `Product Category` field during the post-initialization phase.

Testing
=======

Test the following scenarios:

- **Product Variant Form View**:
  
  - Ensure the `Product Category` field is visible and correctly populated in the product variant form.

- **Product Tree View**:
  
  - Verify that the `Product Category` field appears in the product tree view.

- **Post Initialization**:
  
  - After installation, check that the `Product Category` field is correctly populated for all products based on their templates.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
