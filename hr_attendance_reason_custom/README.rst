.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

===========================
HR Attendance Reason Custom
===========================

Overview
========

The **HR Attendance Reason Custom** module enhances the attendance management process in Odoo by allowing employees to perform a **sign-in** or **sign-out** action without having to select a reason, under certain conditions.  
This behavior is particularly useful when no valid reasons are available for selection.

Features
========

- Allows **sign-in** or **sign-out** without a selected reason if no reasons are configured.

- Ensures that an attendance reason is only required if valid options are available.

- Customizes the attendance screen by considering the employee's attendance state (`checked_in`, `checked_out`) and the available attendance reasons.

Usage
=====

1. **Install the Module**:

   - Install the **HR Attendance Reason Custom** module from the Apps menu.

2. **Sign In / Sign Out**:

   - When an employee is **checked in** or **checked out**, and if there are no reasons available for selection, the employee can perform the **sign-in** or **sign-out** action without choosing a reason.

3. **Reason Requirements**:

   - If valid reasons are configured and available, the employee will be prompted to select one when signing in or out.

4. **Notifications**:

   - If the reason is required and not selected, a notification will be displayed asking the employee to select a reason.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/sale-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
