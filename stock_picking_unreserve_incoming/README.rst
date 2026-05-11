.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================================
Stock Picking Unreserve Incoming
===================================

By default, Odoo hides the **Unreserve** button on incoming transfers
(receipts). This module removes that restriction so the button is visible
on any transfer type, as long as there is reserved stock to release
(state ``assigned`` or ``partially_available``).

For pickings with ``move_type = one`` (ship all at once), the button is
also shown in state ``confirmed``, consistent with the behaviour on
outgoing transfers.

The button remains hidden on immediate transfers (``immediate_transfer = True``).

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>