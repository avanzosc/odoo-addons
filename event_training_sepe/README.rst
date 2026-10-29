.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================
Event Training Sepe
===================

The **Event Training Sepe** module allows users to manage training funding records, training actions, and training events in Odoo 18. It also provides a catalog of SEPE training specialties that can be imported from Excel or CSV files.

The module establishes a hierarchical relationship between funding records, training actions, and events, allowing users to organize and track training activities and their associated funding information.

Features
========

- Manage **Training Funding Records**, including grants, tenders, agreements, and contracts.

- Manage **Training Actions** associated with funding records, including academic information, training hours, delivery modalities, planned attendees, and allocated amounts.

- Link multiple training actions to a funding record and multiple events to a training action.

- Extend **Events** with related training information, including funding details, training action codes, SEPE specialty codes, delivery modalities, and training hours.

- Automatically display related funding and training information in events through read-only fields.

- Manage a **SEPE Training Specialties Catalog**, including specialty codes, names, versions, professional families, professional areas, qualification levels, delivery modalities, durations, and related occupations.

- Import SEPE training specialties from Excel or CSV files, preserving catalog codes and descriptions.

- Support multiple versions of the same specialty code.

- Track funding records and training actions through their corresponding status fields.

- Provide access to internal Odoo users.

Usage
=====

1. **Install the Module**:

   - Copy the `event_training_e` directory into the Odoo addons path.

   - Update the Apps list and install the **Event Training Sepe** module.

2. **Manage Training Funding Records**:

   - Navigate to **Formación SEPE > Expedientes**.

   - Create a funding record and specify its code,

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
* Berezi Amubieta Eceiza <bereziamubieta@avanzosc.es>
