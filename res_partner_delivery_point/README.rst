.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================
Res Partner Delivery Point
==========================

This module enhances the functionality of Odoo's Sales Orders by automatically setting the shipping address based on a designated "Pick Up Point" assigned to the customer. If a customer has a specific pick up point defined, that pick up point will be used as the shipping address for their orders.

Usage
-----

The module achieves this behavior through the following modifications to the `sale.order` model:

- **`onchange_partner_id` method**: This method is triggered whenever the `partner_id` field changes in the Sales Order form. It checks if the customer (`partner_id`) has a `delivery_point` assigned. If so, it sets `partner_shipping_id` to this pick up point.

- **`create` method**: This method is overridden to intercept the creation of new Sales Orders (`sale.order`). If a `partner_id` is provided but `partner_shipping_id` is not specified, it checks if the associated partner (`res.partner`) has a `delivery_point`. If yes, it assigns this pick up point as `partner_shipping_id`.

- **`write` method**: This method is overridden to handle updates to existing Sales Orders. If `partner_id` is included in the update and `partner_shipping_id` is not specified, it checks if the associated partner (`res.partner`) has a `delivery_point`. If yes, it assigns this pick up point as `partner_shipping_id`.


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
* Unai Beristain <unaiberistain@avanzosc.es>
