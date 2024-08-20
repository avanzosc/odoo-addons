.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


===========================================
CRM Lead Lost Reason Additional Information
===========================================

This module extends the CRM lead management system in Odoo by adding additional fields to capture detailed information about lost opportunities. It includes enhancements to both the lead form and the lost reason wizard to include competitor-related details.

Features
========

- **Extended CRM Lead Form**: 
  Adds new fields to the CRM lead form to capture information about competitors when a lead is marked as lost. The fields include:
  - Competitor Manufacturer
  - Competitor Integrator
  - Competitor Reseller
  - Competitor Price
  - Lost Reason Notes

- **Enhanced Lost Reason Wizard**: 
  Includes the new fields in the lost reason wizard, allowing users to update or provide additional details when a lead is marked as lost.

- **Automatic Field Population**: 
  The wizard automatically populates the fields with information from the CRM lead record when opening the wizard.

Usage
=====

Once installed, the module will:
1. **Extend the CRM Lead Form**:
   - Navigate to CRM > Leads.
   - Open a lead and check the "Competitor Details" group in the form view.

2. **Enhance the Lost Reason Wizard**:
   - When marking a lead as lost, the wizard will now include additional fields for competitor information and lost reason notes.

Configuration
=============

No specific configuration is required. The module will automatically integrate with the existing CRM lead and lost reason views.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please check there if your issue has already been reported. If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.

License
=======
This project is licensed under the AGPL-3 License. For more details, please refer to the LICENSE file or visit <http://www.gnu.org/licenses/agpl-3.0-standalone.html>.
