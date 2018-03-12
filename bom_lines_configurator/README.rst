.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
BOM line configurator
=====================

Adds 2 new tables on Bom lines to add formulas and conditions that are
evaluated when we produce or plan a production order.

One of the tables is to calculate custom quantity of a product in a
particular conditions and the other to calculate attribute values of
the template given in the bom line.

In formula or conditions, we use values of the product to be produce. It
will be reference using the value code.

There are some reserved words in the case of attribute value evaluation. We
can use 'self' to reference a value of attribute specified on configuration
line or 'const' to reference a constant value specified on
constants table, the latter created on this module.

Examples (attribute value):

Attribute ------------------- Formula (reverse polish notation) ------Condition(odoo domain)

attr1                         val1 val2 +                             [True]
attr2                         const.val1 self.val1 *                  [(val1, '=', 1), '|',(val2, '<', 2), (val2, '>=', 10)]
attr2                         const.val1 self.val1 +                  [True]

In the first case the values of the product to produce (val1, val2) will be
summed and if exits a value of attr1 with this value will be assigned.

In the second case will multiply the 'val1' of the constant table and the
'val2' of 'attr2'. Only when the val1 of the product to produce is equal to
one and the val2 is less than 2 or greater or equal to 10.

The third case only is evaluated if the second is not satisfied

In quantity configuration table we have only two columns formula and
conditions. The result of formula is multiplied with the quantity of bom line.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/8.0


Credits
=======

Contributors
------------
* Mikel Arregi <mikelarregi@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>