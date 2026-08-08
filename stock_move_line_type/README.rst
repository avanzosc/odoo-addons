.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====================
Stock Move Line Type
====================

This module adds a computed ``Move Line Type`` field to stock move lines,
classifying each line based on the usage of its source and destination locations:

- **Incoming**: source is not internal, destination is internal.
- **Outgoing**: source is internal, destination is not internal (not scrap).
- **Expired**: source is internal, destination is a scrap location.
- **Internal**: both source and destination are internal.
- **Other**: any other combination.

The field is stored and enables filtering and grouping directly from the
detailed operations view. New search filters (*Incoming*, *Outgoing*,
*Internal*, *Expired*, *Other*) and a *Group By Move Line Type* option
are added to the stock move line search view.

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
