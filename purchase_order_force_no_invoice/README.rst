.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

===============================
Purchase Order Force No Invoice
===============================

This module allows forcing the billing status of a purchase order to
"Nothing to Bill", even if there are order lines or quantities still
pending billing.

The standard ``invoice_status`` field on ``purchase.order`` is computed
and stored, so it cannot be set directly. This module adds a boolean
field, ``Force Nothing to Bill``, and extends the computation so that,
when checked, the order's billing status is always set to "Nothing to
Bill" regardless of the state of its lines.

**Usage**

#. Open a purchase order.
#. Go to the *Other Information* tab, *Billing* section.
#. Check the *Force Nothing to Bill* field.
#. The order's *Billing Status* is recomputed to "Nothing to Bill" and
   the order stops appearing in the "Waiting Bills" filters and views.
#. Unchecking the field restores the standard computation.

Note: this only affects the order's billing status. It does not prevent
billing the pending quantity if a user manually creates a vendor bill
from the order.

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
