This module allows you to identify products that have FSC (Forest Stewardship Council) certification.

The module adds the following functionality:

* Adds a boolean field "Is FSC certificate" in product template to mark products with FSC certification.

* Automatically propagates the FSC status to commercial documents:

  * **Sale Orders**: Computes whether any line contains an FSC-certified product.
  * **Delivery Orders**: Computes whether any move contains an FSC-certified product.
  * **Invoices**: Computes whether any invoice line contains an FSC-certified product.

* Modifies reports to display the FSC certification:

  * Adds an asterisk (*) next to FSC-certified product names in line items.
  * Displays the FSC certificate logo and number at the bottom of documents.
  * Applies to: Sale Order reports, Delivery Slip, and Invoice reports.

* Adds a server action "FSC Update Orders" to recalculate FSC status for selected products.

The FSC certification mark and number are configured at the company level, allowing each company to display its own certification details.
