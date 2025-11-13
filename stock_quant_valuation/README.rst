.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=====================
Stock Quant Valuation
=====================

This module extends the **Stock Quant** model to provide additional cost and valuation information for inventory quants.  

**Features**

- **Product Cost**: Displays the standard price of the product related to the quant.
- **Lot Purchase Cost**:  
  Uses the purchase cost from the linked lot if available, otherwise falls back to the product's standard price.
- **Lot Purchase Value**:  
  Calculates the total valuation of the quant based on its quantity and the lot purchase cost.

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

