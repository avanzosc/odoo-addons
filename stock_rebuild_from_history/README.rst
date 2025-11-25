.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================================
Stock Rebuild From History
=================================

This module adds a **“Rebuild Stock”** button to the product template form.  
Its purpose is to recalculate product quants based on all **completed stock move lines**.

### Features
- Resets the quantities of existing quants for the product and its variants.
- Recomputes stock levels by reading all `done` move lines.
- Updates or creates quants for each combination of:
  - Source & destination locations  
  - Lot/serial  
  - Package  
  - Owner  
- Ensures stock data is rebuilt accurately without deleting any quant records.

### Usage
From the product template form, click **Rebuild Stock**.  
The module will:
1. Set all related quants to `0`.
2. Replay all done stock movements.
3. Adjust quantities according to each move's source and destination.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



