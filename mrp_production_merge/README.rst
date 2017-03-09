.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Manufacturing Order Merge
=========================

With this module you can merge into one manufacturing order those 'draft'
orders that have the same:

* Product
* Unit of Measure
* Bill of Material
* Routing (if the order does not have a routing but it has in its BoM, it
  will be taken as the routing)

The quantity will be increased in one of the selected orders and planned date
will be adjusted to the one in the wizard, other orders will be cancelled.

Credits
=======

Contributors
------------

* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
