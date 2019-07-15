.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Stock Picking Service Sale
==========================

New module to charge services in pickings.
 - New service line object, each line has a direct link to sale line,
   shows sale line's unit price, quantity, discount and subtotal fields and
   a check which when is deactivated moves the service line to the backorder picking.
 - When a picking is created from a sale order, the system will create one service
   line related to this picking for each line in the sale order with service product.
 - When transfering a partial picking, all the lines with deactivated check will be
   moved to the backorder picking. And all lines with activated check will stay in
   the transferred picking.
 - In picking valuation will sum all service charges.
 - When invoicing a picking, the system will not invoice all service lines in the
   sale order, only the lines related to the picking.
 - The service lines will be displayed in the picking report.


Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
