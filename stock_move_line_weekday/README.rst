.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================
Stock Move Line Weekday
=======================

This module extends stock move lines with date breakdown, warehouse and
minimum quantity fields derived from reordering rules.

The following fields are automatically computed and stored on each move line,
using ``date_done`` of the picking when available and falling back to the
line's own ``date``:

- **Weekday**: day of the week (Monday to Sunday).
- **Week**: ISO week number of the year.
- **Month**: month of the year (January to December).
- **Year**: year of the operation.
- **Warehouse**: warehouse derived from the picking operation type.
- **Minimum Quantity**: minimum quantity from the applicable reordering rule,
  resolved in priority order: specific-date weekday rule → weekday rule →
  default orderpoint minimum quantity.

New group-by options (*Year*, *Month*, *Week*, *Weekday*, *Warehouse*) are
added to the stock move line search view. A pivot view is also included,
pre-configured with product and weekday as rows, warehouse as columns, and
``Quantity Done`` and ``Minimum Quantity`` as measures.

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