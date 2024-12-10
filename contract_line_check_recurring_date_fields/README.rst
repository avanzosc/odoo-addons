.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=========================================
Contract Line Check Recurring Date Fields
=========================================

Overview
========

The **Contract Line Check Recurrence Date Fields** module enhances the contract management system by applying onchange functionality to contract fields. This ensures that when the `line_recurrence` field is inactive, the associated line fields in `contract.line` are updated automatically based on the contract's values.

Features
========

- **Automatic Updates**: Fields in contract lines (`date_start`, `date_end`, `is_terminated`, `terminate_date`, `last_date_invoiced`, `recurring_interval`, `next_period_date_start`, `next_period_date_end`) are updated automatically when the corresponding contract fields change and `line_recurrence` is inactive.
  
Usage
=====

1. **Install the Module**:

   - Install the module via Odoo's Apps interface.

2. **Updating Contract Lines**:

   - When editing a contract, modifying fields like `date_start`, `date_end`, or others will automatically update the associated contract lines if `line_recurrence` is not active.

Configuration
=============

No additional configuration is required. The module works out of the box.

Testing
=======

Test the following scenarios:

- **Field Update on Contract Change**:

  - Create or edit a contract and modify fields such as `date_start`, `date_end`, etc.
  - Ensure that the corresponding fields in the `contract.line` records are updated correctly when `line_recurrence` is inactive.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

For module-specific questions, please contact the contributors directly. Support requests should be made through the official channels.

License
=======

This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
