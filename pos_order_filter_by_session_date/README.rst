.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

================================
POS Order Filter By Session Date
================================

This module filters the open tickets shown in the POS interface to only
display those created on the same date or after as the current session opening.
This prevents old draft orders from previous sessions accumulating in the
order tabs and causing severe performance degradation on startup.

The filtering is applied at three levels:

* **IndexedDB (browser cache)**: old draft orders from previous sessions are
  excluded before being loaded into the Owl reactive model, preventing the
  browser from hanging when the local cache contains thousands of stale orders.
* **Device synchronisation domain**: the domain sent to
  ``read_config_open_orders`` is built directly from the session date instead
  of iterating all cached records, avoiding the construction of huge
  ``Domain.or()`` arrays.
* **Server side**: ``read_config_open_orders`` applies the session date filter
  as a safety net, ensuring only today's orders are returned regardless of the
  client domain.

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
