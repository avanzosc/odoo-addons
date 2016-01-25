.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

====================================
Sale service recurrence configurator
====================================

* On the lines of sales order template, are defined Boolean fields for the
  months of the year, for 5 weeks, and for the days of the week.
* When the template is selected in the sales order, the information in these
  new fields, is charged to the sales order lines.
* Created in product object, the new field "Recurring Service". This new field
  will only be visible to the product-type "service".
* By selecting the product in sale order line, if recurring service of the
  product is equal to false, the checks of months, weeks and days are hidden.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
