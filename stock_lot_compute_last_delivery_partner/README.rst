.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================================
Stock lot compute last delivery partner
=======================================

* Change the "compute" function of the "Last Delivery Partner" field in lots.
* The move line with the most recent date for that lot, and whose status is
  equal to "done", will be searched for.
* If the move line found has a picking and is of type "outgoint", the partner
  of the picking will be taken, otherwise nothing.

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
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
