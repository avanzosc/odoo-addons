.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==================
Event with commute
==================

* In events new tab to be able to define products "displacement".
* To define a displacement type product, you must create a product with the
  following attributes: Product Type (Service), Service Invoicing Policy: 
  Timesheets on tasks, Service Tracking: Create a task in sales order's
  project. A line must be created on the sales order with this product. 
* When the event is confirmed, the sale order line with the "Displacement"
  product will be brought to the "Displacement products" tab of the event.
* When the session is marked as "Done", an accounting entry will be registered
  for each line of the "Displacement products" tab of the event. 

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
* Afredo de la Fuente <alfredodelafuente@avanzosc.es>
