.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=====================
Account Analytic Menu
=====================

By default, Odoo only exposes *Analytic Accounts* under *Invoicing >
Configuration > Analytic Accounting*, a menu restricted to the
``account.group_account_manager`` group (since the whole *Configuration*
section requires it). Regular accounting users, who only have
``account.group_account_invoice`` or ``account.group_account_readonly``,
cannot reach it at all.

This module adds a top-level *Analytic* menu directly under *Invoicing /
Accounting*, next to *Customers*, *Vendors*, *Accounting* and *Reporting*,
with an *Analytic Accounts* entry pointing to the same action used by the
existing technical menu. It also grants read/write/create/unlink access
on ``account.analytic.account`` to both accounting groups, since the
model's access rules were otherwise limited to the technical
``analytic.group_analytic_accounting`` group.

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

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
