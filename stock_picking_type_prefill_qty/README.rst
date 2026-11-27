.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===================================
Stock Picking Type Prefill Quantity
===================================

In standard Odoo, the quantity of a stock move (``stock.move.quantity``,
and the underlying ``stock.move.line.quantity``) is used both as the
reserved quantity and as the quantity actually done. Whenever a move is
reserved against a location that doesn't hold real stock (typically the
vendor location on a purchase receipt, which is considered to have
unlimited availability), Odoo has nothing real to reserve and fills that
quantity with the full amount demanded. In practice this means receipts
(and any other operation reserved the same way) open with the quantity
already set to the full ordered amount, ready to validate as is.

This module adds a "Prefill Quantity" checkbox on the operation type
(``stock.picking.type``), checked by default so nothing changes out of
the box:

* Checked (default): standard Odoo behavior, the quantity is auto-filled
  with the full demand on reservation.
* Unchecked: the quantity is left at 0 for moves of that operation type
  reserved against a location without real stock, so it has to be
  entered manually with what was actually done.

Uncheck it on the "Receipts" operation type used for purchases so the
quantity has to be entered manually there, without affecting any other
operation type.

For now the checkbox is only shown on receipt operation types
(``code = 'incoming'``), since that's the only case currently needed:
on deliveries or internal transfers the source is normally a real
warehouse location, so the quantity there comes from an actual stock
reservation and the checkbox would have no effect. The field and the
logic behind it are otherwise generic to any operation type, so if
sales or manufacturing ever need the same behavior (e.g. a delivery or
production move reserved against a location without real stock), it's
just a matter of showing the field for those ``code`` values too in
``views/stock_picking_type_views.xml``, no model changes needed.

Known limitation: if a move line for the same product/locations already
exists on the move before it is reserved again (e.g. a line added
manually before checking availability), its quantity is topped up
directly by the reservation logic without going through this module's
code, so it keeps the standard behavior in that specific case.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
