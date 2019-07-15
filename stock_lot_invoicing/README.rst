.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Stock Lot Invoicing
===================

New module to invoice by lot and lot prices.

* New unit_price, cost_price and percentage fields in lots.

  * Cost_price = Unit_price * percentage/100

* When invoicing purchases, invoice line price = lot's cost_price.
* When invoicing sales, invoice line price = lot's unit_price.
* When transfer purchases, must define lot's percentage.
* When transfer sales, must define lot's unit_price.


Credits
=======

Contributors
------------

* Ainara Galdona <ainaragaldona@avanzosc.es>
