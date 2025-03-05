.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: AGPL-3

==============================
HR Leave Unusual Days Holidays
==============================

Overview
========

The **HR Leave Unusual Days Holidays** module extends the HR Leave functionality to consider bank holidays as unusual days. It ensures that bank holidays, which are typically shown on the right side of the calendar, also appear in gray as unusual days, making it easier to manage leaves during these special days.

Features
========

- Extends the `hr.leave` model by overriding the `get_unusual_days` method.
- Includes bank holidays in the list of unusual days when calculating leaves.
- Displays bank holidays in the calendar view alongside other unusual days.

Usage
=====

This module works automatically after installation. When calculating the unusual days for a leave request, bank holidays will be included as unusual days, and they will appear in the same way as regular unusual days on the calendar.

Configuration
=============

No additional configuration is needed. The system will automatically integrate bank holidays into the leave calendar.

Testing
=======

1. Create a leave request for an employee, specifying a date range that includes bank holidays.
2. Ensure that the bank holidays are included as unusual days in the calendar view.

Bug Tracker
===========

Bugs and issues can be reported on the GitHub repository:
`GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For further information, please contact the contributors.

License
=======

This project is licensed under the AGPL-3 License.
For more details, see the LICENSE file or visit:
<https://www.gnu.org/licenses/agpl-3.0.html>.
