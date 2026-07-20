.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Stock Picking Report Valued Ext
===============================

This module extends ``stock_picking_report_valued`` with two improvements:

**Editable valued flag on the picking**

- The *Valued* field becomes an independent, editable boolean stored on
  each picking instead of being a read-only related field pointing to the
  partner.
- When a picking is created, the field is automatically initialized from
  the *Valued Picking* flag of the delivery address.
- When the delivery address is changed on a picking, the field updates
  accordingly.
- The field is displayed in the picking form header, allowing users to
  enable or disable valued printing directly on the delivery slip.

**Valued Picking flag visible when creating addresses**

- The *Valued Picking* check is shown in the address form that opens when
  adding a new address from within a customer record, for address types
  *Delivery Address* and *Other Address*, so users can configure it at
  creation time without having to open the contact separately afterwards.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
