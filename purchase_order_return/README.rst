.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=====================
Purchase Order Return
=====================

This module extends the Purchase Order functionality to allow specifying return quantities directly on purchase order lines, and automatically creates return pickings based on those quantities.

Key Features
============

- **Return Quantity Field (`return_qty`)**: Dedicated field to register quantities to be returned on purchase order lines
- **Smart Picking Management**: Automatic creation and updating of reception and return pickings based on quantity changes
- **Respects Done States**: Never modifies pickings that are already in DONE state, always creates new ones for remaining quantities
- **"Validate Everything" Button**: Single button to confirm and validate all pending pickings for an order

1. **Reception Quantities Handling**
When values are entered in the **Quantity** column:

- **If a pending reception picking exists:** The picking will be updated, either by adding a new line or updating the existing one.
- **If a reception picking exists but is already DONE:** It will not be modified at all. A new picking will always be created for any remaining quantities to be received.

2. **Return Quantities Handling**
When values are entered in the **To Return (return_qty)** column:

- **If a pending return picking exists:** The picking will be updated, either by adding a new line or updating the existing one.
- **If a return picking exists but is already DONE:** It will not be modified at all. A new picking will always be created for any remaining quantities to be returned.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
