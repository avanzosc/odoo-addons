.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

================================
Purchase Order List Column Width
================================

This module fixes the width of the two label-less columns that Odoo places at
the beginning of the purchase order lists, so that they stop stealing
horizontal space from the rest of the columns.

Those columns are:

* The **priority** star column (``priority``, declared with ``nolabel="1"``).
* The **Has Alternatives** button column added by ``purchase_requisition``.

Neither of them declares a width, so Odoo falls back to a minimum of 80px with
no maximum, and both columns absorb the leftover space when the list is
stretched to fill the available width. They cannot be resized by dragging
either, because the resize handle is only rendered for columns that have a
label. On top of that, the button column is never shrinkable, so it keeps its
width even when the rest of the list is squeezed.

Setting an explicit ``width`` in the arch makes Odoo use it as both the minimum
and the maximum width of the column, which removes the problem.

Key features
============

* ``priority`` column fixed to 30px in *Requests for Quotation*, in
  *Purchase Orders* and in the plain purchase order list.
* **Has Alternatives** button column fixed to 30px. The button is kept, only
  its column width is limited.

Usage / How to test
====================

1. Go to **Purchase -> Orders -> Requests for Quotation** in list view.
2. The blank space between the selection checkbox and the **Reference** column
   is now reduced, and the remaining columns get that space back.
3. The behaviour is the same with the priority column shown or hidden from the
   optional columns dropdown.

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
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
