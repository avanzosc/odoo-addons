.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==========================
Custom Breeding MRP Report
==========================

Glue module between **MRP** and **Breeding**, extending the existing Breeding XLSX report with manufacturing data.

It adds the concept of *Seized Units* coming from manufacturing orders linked to a breeding batch and computes the corresponding *Seized Percentage* based on the batch output units.

Main features
-------------

- Computes seized units for each ``stock.picking.batch`` from related ``mrp.production`` records.
- Calculates the seized percentage automatically.
- Displays the seized percentage in batch form and tree views.
- Extends the existing *Breeding Report* XLSX by adding a new column **Seized %**, including a total calculation.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/mrp-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.



