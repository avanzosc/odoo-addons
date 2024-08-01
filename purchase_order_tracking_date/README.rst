.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Purchase Order Tracking Date
============================

This Odoo module adds a "Purchase Tracking" tab to Purchase Orders to help control and monitor the time from when a purchase order is launched until it is received in the warehouse.

Features
--------

- Adds a "Purchase Tracking" tab to the Purchase Order form.
- Allows selection of the following fields:

  - Forwarder (transportation service provider)
  - Carrier (company responsible for the vessel)
  - Port of Origin (POL)
  - Port of Destination (POD)

- Tracks important dates for the purchase order process:

  - Date Sent
  - Date of Confirmation (existing field)
  - Cargo Ready Date
  - Cut-off Date
  - Estimated Time of Departure (ETD)
  - Estimated Time of Arrival (ETA)
  - Date of Delivery in Warehouse (existing field)

Usage
-----

1. Navigate to Purchase -> Purchase Orders.
2. Create a new Purchase Order or edit an existing one.
3. Open the "Purchase Tracking" tab to fill in the tracking information.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
