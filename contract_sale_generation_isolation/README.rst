.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==================================
Contract Sale Generation Isolation
==================================

This module makes the recurring sale order generation from contracts
(``contract_sale_generation``) resilient to failures, instead of an
all-or-nothing daily batch.

By default, the scheduled action that generates sale orders from due
contracts builds and confirms every order of the batch in a single
operation, with no commit in between. In practice this means that if one
contract has invalid data, the whole batch fails and **no** contract gets
its sale order that day, not just the broken one.

This module processes contracts one at a time instead, so a single
broken contract no longer affects the rest of the batch. It also commits
after each contract, so that if the process is interrupted for any
reason (for example, if the batch is large enough to exceed the worker's
time limit, ``limit_time_real`` / ``limit_time_real_cron``), whatever was
already generated is not lost.

Configuration
=============

Go to *Settings > General Settings > Contract* and, under *Exception
Responsible*, pick the user who should be notified when a contract fails
to generate its recurring sale order. If left empty, the contract's own
responsible user is notified instead.

Usage
=====

The module runs automatically as part of the existing
*Generate Recurring sales from Contracts* scheduled action, or any other
scheduled action / server action that ends up calling
``recurring_create_sale()`` on contracts, whether it is given the whole
batch at once or called contract by contract in its own loop. No manual
action is required for it to work.

* Each contract is generated in isolation. If it fails, only that
  contract's changes are rolled back; the rest of the batch continues.
* Before and after each contract, the transaction is committed for real,
  so progress is not lost if the process is interrupted afterwards, and
  a failure is not affected by any commit that downstream automations
  (report generation, outgoing mail, ...) may trigger on their own while
  generating the sale order.
* A contract that fails is flagged (visible as a red ribbon on its form
  view, with the error detail and date) and is skipped by future runs
  until the issue is resolved. An activity is also created for the
  configured responsible user.
* Use the *In Generation Error* filter on the contracts list to find all
  flagged contracts.
* Once the underlying issue is fixed, open the contract and click
  *Mark as Resolved* to clear the flag and make it eligible again for
  the next run.

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
* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
