.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=============================
L10n ES TicketBAI API Disable
=============================

Overview
========

The **L10n ES TicketBAI API Disable** module disables the TicketBAI invoice sending functionality in Odoo. This allows users to bypass the automatic submission of invoices to the TicketBAI system, which can be useful for testing or in cases where compliance is not yet mandatory. Additionally, it ensures that the TicketBAI functionality remains disabled for all companies.

Features
========

- **Disable Invoice Submission**: Overrides the `send` and `send_pending_invoices` methods of the `tbai.invoice` model to prevent automatic submission.
- **Enforce Disabled State**: The existing `tbai_enabled` boolean field in the `res.company` model is always set to `False`, ensuring that TicketBAI functionality cannot be enabled.
- **Post-Initialization Hook**: Uses a post-initialization hook to set the `tbai_enabled` field to `False` for all companies in the system.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Invoice Submission Disabled**:

   - Once installed, the automatic submission of invoices to TicketBAI will be disabled.

3. **Company Setting**:

   - The `tbai_enabled` field in the company settings will always be set to `False`, preventing users from enabling the TicketBAI functionality.

Configuration
=============

- **No additional configuration is required** for this module. It simply prevents the sending of TicketBAI invoices and ensures that TicketBAI functionality cannot be enabled.

Testing
=======

Test the following scenarios:

- **Invoice Processing**:

  - Create and validate an invoice to ensure that it is not submitted to the TicketBAI system.

- **Company Settings**:

  - Verify that the `tbai_enabled` field in company settings remains `False` and cannot be changed.

Bug Tracker
===========

For bugs and issues, please visit `GitHub Issues <https://github.com/avanzosc/l10n-addons/issues>`_ to report or track issues.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Please contact contributors for module-specific questions, but direct support requests should be made through the official channels.

License
=======
This project is licensed under the LGPL-3 License. For more details, please refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
