.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

======================================
Contract Line Error Tracking
======================================

Overview
========

The **Contract Line Error Tracking** module extends the functionality of the existing contract module by adding error tracking capabilities to contract lines. This enhancement allows for better error management and ensures that contract processing can continue even if errors occur in specific lines.

Features
========

- **Error Tracking**: Introduces a new boolean field `error_occurred` to the `contract.line` model, which is used to indicate whether an error has occurred in the processing of a specific contract line.

- **Validation Logic**: Extends the `_check_recurring_next_date_start_date` method to check if the `date_start` is after the `recurring_next_date`. If this condition is met, the `error_occurred` field is set to `True`, and an error message is logged.

- **User Interface Updates**: Inherits and modifies the existing contract line form and tree views to display the `error_occurred` field, allowing users to easily see which lines have encountered errors.

Usage
=====

1. **Install the Module**:

   - Install the module through the Odoo apps interface or by placing it in your Odoo addons directory.

2. **Error Indication**:

   - The `error_occurred` field will automatically be set to `True` when a validation error is detected in the contract line processing.

3. **User Interface**:

   - The error status can be viewed in both the form and tree views of the contract lines, making it easy to identify which lines have issues.

Configuration
=============

- **No additional configuration is required** for this module. The error tracking functionality is integrated seamlessly with the existing contract management processes.

Testing
=======

Test the following scenarios:

- **Contract Line Validation**:

  - Create and manage contract lines to verify that the `error_occurred` field is set correctly when a validation error occurs.

- **User Interface Check**:

  - Ensure that the `error_occurred` field is visible in both the form and tree views of contract lines.

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
