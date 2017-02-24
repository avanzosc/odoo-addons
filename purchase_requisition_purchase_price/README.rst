.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================================
Purchase requisition purchase price
===================================
* In "Products" of "Purchase requisition", new field "Purchase price". Each
  "Product" line will be associated with the purchase line generated.
* When you change the quantity or unit price of a purchase line associated with
  a "Product" of "Purchase requisition", the "Purchase price" field of
  "Purchase requisition" will be changed, taking all the purchase order lines,
  associated with the "Product" of "Purchase requisition", in ascending order
  by price unit , to cover the necessary amount.
* If all amount of the purchase line has been used, it will appear in green, if
  a partial quantity has been used, the purchase line will appear in blue.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>