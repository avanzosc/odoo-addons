.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Stock Location Warehouse Change
===============================

* When the parent location of a location changes, the warehouse of the
  location and of all its child locations, archived ones included, is updated
  to the warehouse of the new parent location.
* The warehouse is shown in the location form and is updated as soon as the
  parent location is changed, before saving.
* New group "Location Warehouse Editor" (Extra Rights). Only the users of this
  group can change the parent location of a location when its warehouse
  changes. The rest of the users can still change the parent location inside
  the same warehouse.
* New action "Recompute Warehouse" in the locations list and form, available
  only for the users of the group. It recomputes the warehouse of the selected
  locations and of all their child locations, archived ones included.


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
