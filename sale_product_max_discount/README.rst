.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Sale Product Maximun Discount
=============================

* New minimun margin field in products.
* New computed field in products named 'maximun discount', its formula is the
  below one:
  ((List Price - Standard Price) - (Minimun margin * List Price)) / List Price
* New state in sales workflow. When any of sale lines have exceeded the maximun
  discount defined in the products form, when confirming the order, it will pass
  to validation state, and only the sales manager will be able to confirm the
  order in that state. However, when there is no sale line which exceedes the
  maximun discount defined in the product form, the order will pass to confirmed
  state directly when confirming it.

Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
