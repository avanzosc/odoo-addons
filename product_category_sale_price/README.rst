.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Product category sale price
===========================

* New permission group "Allow change sales price on products".
* In Sales - Configuration, new menu "Product categories sale price", for new
  object "Product category sale price". This new object have the fields: 
  name, % Discount, fixed amount. From the form of this new object you can
  navigate to its related products.
* In products new fields:Product category sale price, target cost, manual PSP,
  last price change date.
* Whenever you change the Target Cost, Extra Cost, Sales Price Category fields
  in products, the sale price of the product will be calculated as follows:
  PSP = (target cost) *% discount of the price category + Fixed amount field of
  the sale price category
* In products 2 new actions to assign category for sale price, and to
  change manual PsP. In order to do any of these 2 actions, the user
  must belong to the group created in this module. If a user is not in this
  group, the fields referenced will be read-only.
*


Bug Tracker
===========


Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
