.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Website Visitor Usability
=========================

* In the menu Website / Reporting / Visitors, the search view of the
  ``website.visitor`` model only offered a fixed "Last 7 Days" filter on the
  "Last Connection" date and a flat group by on that same field, without the
  ability to drill down by month, quarter or year.
* This module extends the search view of ``website.visitor`` so that the
  "Last Connection" and "First Connection" dates are exposed as standard Odoo
  date filters with the month / quarter / year cascade (the same behavior used
  in other reports such as Purchase Orders).
* The same date fields are also added to the "Group By" section as proper
  date group-by filters, so the records can be aggregated by day, week, month,
  quarter or year.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.com>

Do not contact contributors directly about support or help with technical issues.
