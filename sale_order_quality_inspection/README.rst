.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=============================
Sale Order Quality Inspection
=============================

This module adds a shortcut button on sale orders to navigate to all quality
inspections associated with the order.

**Features**

- **Quality Inspections Shortcut**
  - Adds a stat button on the sale order form showing the total count of
    related quality inspections.
  - Clicking the button opens the list of inspections filtered to those linked
    to the order's manufacturing orders (via ``mrp_sale_info``) and its
    delivery pickings (via ``quality_control_stock_oca``).

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.