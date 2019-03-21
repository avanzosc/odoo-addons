.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Stock Inventory Line Ext
========================

* New field on stock_inventory_line
    - Standard_price = Product's standar price
    - Value = Standard_price multiplied by quantity
    - Under_repair = Sum of amount of the repair lines in which the product
        appears
    - Net_qty = Theorical quantity minus under_repair quantity
    - Net_value =  net_qty multiplied by standar_price

Credits
=======

Contributors
------------

* Esther Martín <esthermartin@avanzosc.es>

