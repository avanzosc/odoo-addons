.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
Stock Warehouse Orderpoint Forecast and Pending Qty
===================================================

Overview
========

The **Stock Warehouse Orderpoint Forecast and Pending Qty** module enhances the stock management system in Odoo by adding additional fields to the stock warehouse orderpoint list view. This module provides better visibility into forecasted and pending quantities for orderpoints, which aids in more effective inventory management and planning.

Features
========

- **Forecast Quantity Field**:
  - Adds a `forecast_qty` field to the orderpoint list view, which displays the forecasted quantity of products that are expected to be needed.

- **Pending Quantity Field**:
  - Adds a `pending_qty` field to the orderpoint list view, which shows the quantity of products that are currently pending to be fulfilled based on existing orders and forecasts.


Usage
=====

Once installed, the `forecast_qty` and `pending_qty` fields will be visible in the stock warehouse orderpoint list view. This allows users to view and manage these quantities directly from the list, improving the efficiency of inventory management processes.

Configuration
=============

No additional configuration is required. The fields will automatically appear in the orderpoint list view once the module is installed.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_. If you encounter any issues, please check there to see if your issue has already been reported. If not, provide detailed feedback to help us resolve it.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.

License
=======
This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <http://www.gnu.org/licenses/agpl-3.0-standalone.html>.
