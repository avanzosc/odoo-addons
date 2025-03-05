.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=========================
Res Partner Product Promo
=========================

Overview
========

The **Res Partner Product Promo** module introduces functionality to associate a promotional product with a partner (customer or supplier). This allows sales orders to automatically assign a specific promotional product to the partner when creating a sale order line.

Features
========

- Adds a new field `promo_product_id` to the `res.partner` model, allowing the association of a promotional product.
- Extends the `sale.order.line` model with a method `action_assign_promo_product_id`, which assigns the promo product to the partner when creating or modifying a sale order line.
- Adds a new section in the partner form view called *Promotions* to manage the promotional product.

Usage
=====

1. **Setup Promo Product for Partners**:
   
   - Go to *Sales > Customers*.
   
   - Open a partner record and select a promotional product from the *Promotions* section.
   
2. **Assign Promo Product to Sale Order**:
   
   - Create a sale order and add a sale order line with a product.
   
   - The system will automatically assign the promotional product from the partner to the sale order line.

3. **Behavior**:
   
   - When a sale order line is added or modified, the promo product will be assigned to the partner.

Configuration
=============

No additional configuration is required to use this module. The promotion product field is added to the partner form view and will be used automatically when processing sales orders.

Testing
=======

1. Open an existing partner record and set a promotional product.
2. Create a sale order for this partner.
3. Add a product to the sale order line.
4. The `promo_product_id` will be automatically assigned to the partner in the sale order.

Bug Tracker
===========

Bugs and issues can be reported on the GitHub repository: 
`GitHub Issues <https://github.com/avanzosc/res_partner_product_promo/issues>`_.

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
<https://opensource.org/licenses/LGPL-3.0>.
