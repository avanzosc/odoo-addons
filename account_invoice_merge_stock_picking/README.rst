.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Account Invoice Merge Stock Picking
===================================

This is a glue module between account_invoice_merge and
stock_picking_invoice_link.
When an invoice created from a picking is merged, its picking_ids will
be replicated in the merged invoice. Although the picking is set as to_invoice
when the origin invoice is cancelled, after the merge it will be set as
invoiced again.

Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
