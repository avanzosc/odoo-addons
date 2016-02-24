.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================
Sale order create event
=======================

* When you are confirming a sales order, creates an Event. For each sales order
  line that has a product of type "service", and this product has the route
  "Generate procurement-task", and is one recursive product, necessary sessions
  are automatically generated. These sessions will be associated with the
  corresponding task.
* You can recalculate the sessions from project task form.
* To register partners in events, the partner should not be my company, not a
  customer, and not a supplier.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>