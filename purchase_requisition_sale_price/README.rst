.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Purchase requisition sale price
===============================

* This module creates a "margin" field in the product of "purchase
  requisition", with this margin the unit sale price is calculated in the
  product of "purchase requisition", and that price is updated in the unit
  price of the sales line associated.
* For calculate margin product line: Unit cos / (1 - margin)
* For calculate purchase requisition margin: 1 - (Total purchase /
  Sale amount_total)

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
