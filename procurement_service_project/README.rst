.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Procurement service project
===========================

* This module creates the new route "Generate procurement-task" for products.

* When you are confirming a sales order that has a product of type "service",
  and this product has the new route "Generate procurement-task", one
  procurement for this service product is created.
 
* Running this procurement, a task is automatically created. If you have
  defined a project in sale order, this project will be assigned to the created
  task.

Credits
=======


Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
