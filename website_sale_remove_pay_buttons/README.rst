.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===============================
Website Sale Remove Pay Buttons
===============================

This module customizes the Odoo eCommerce functionality by removing the "Pay Now" and "Continue to Payment" buttons from the shopping cart page. This ensures that customers can only confirm their cart and continue shopping, without proceeding to the payment step directly from the website.

Usage
-----

The module achieves this behavior through the following modifications to the `website_sale` module templates:

- **Remove 'Pay Now' button**: The button with the ID `o_payment_form_pay` is removed from the DOM using `xpath`.
- **Remove 'Continue to Payment' button**: The button with the class `btn btn-primary btn-lg btn-block` is removed from the DOM using `xpath`.

Installation

Dependencies
------------

This module depends on the following Odoo module:

- `website_sale`

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
