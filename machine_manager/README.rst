.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Machine Manager
===============

Machine Manager is a module for Odoo that allows companies to keep a
complete and organized record of all their physical machinery and equipment.
Whether you own, lease, or rent machines, this module gives you a single
place to manage everything related to them — from basic identification data
to insurance policies and serial numbers.
 
Features
========
 
Machine Registry
----------------
 
The core of the module is the **machine record**, where you can store all
the relevant information about each piece of equipment your company operates.
Each machine record includes:
 
- **Name and identification**: Give each machine a clear name and track its
  manufacturing year, model reference, and frame number.
 
- **Operational status**: Mark each machine as *Active*, *Inactive*, or
  *Out of Service*, so you always know what is available and what is not.
 
- **Ownership type**: Indicate whether the machine is *owned* by your
  company, under a *lease*, or on a *rental* agreement.
 
- **Scope of use**: Classify each machine by its operational scope —
  *Local*, *National*, or *International*.
 
- **Technical details**: Record the machine's power output (in kW),
  MAC address, and phone number if applicable.
 
- **License and documentation**: Store the machine's license or card
  number along with its expiration date, so you can track renewals easily.
 
- **Insurance**: Keep the insurance company name and policy number linked
  directly to each machine record.
 
- **Enrollment date**: Register the date when the machine was formally
  added to your operations.
 
Machine Models (Type Catalogue)
---------------------------------
 
To keep your machine list consistent and well-organised, the module includes
a **Machine Model catalogue**. This lets you define standard model types and assign
them to machines, making it easy to group and filter your equipment by type.
 
Link to Products and Serial Numbers
-------------------------------------
 
Machine Manager integrates with Odoo's existing product and inventory system:
 
- Any serial product in your catalogue can be flagged as **"Can be a Machine"**,
  which makes it available for linking to a machine record. This is useful
  to associate manufacturer information, product category, and other
  product-level data with your machines.
 
- Each machine can be linked to a specific **serial number** from Odoo's
  inventory, giving you traceability between the physical asset and its
  stock record.
 
- From any product's page, a quick-access button shows you at a glance
  **how many machines** are linked to that product, and lets you navigate
  directly to them.
 
Multi-company Support
----------------------
 
Each machine belongs to a specific company within your Odoo database,
making the module fully compatible with **multi-company** setups. Users
will only see machines that belong to their own company.
 
Communication and Activity Tracking
--------------------------------------
 
Every machine record includes Odoo's built-in **chatter**, which means you can:
 
- Log internal notes about a machine.
- Send messages to colleagues directly from the machine record.
- Schedule and track activities (reminders, maintenance follow-ups, calls, etc.).
- See a full history of all interactions related to each machine.
 
Search, Filter, and Group
--------------------------
 
The machine list view supports flexible **searching and grouping** so you
can quickly find what you need:
 
- Search by product, serial number, model, or model type.
- Group machines by model type, model, associated product, or product category.
- All columns in the list view are optional, so each user can show only
  the information that is relevant to them.
 
User and Manager Roles
-----------------------
 
The module defines two access levels under the **Machine Management**
category in Odoo's settings:
 
- **User**: Can view machine and model records but cannot create, edit,
  or delete them.
 
- **Manager**: Has full access to create, edit, and delete both machines
  and model types.
 
This ensures that sensitive records are only modified by authorised staff.
 
Configuration
=============
 
After installing the module:
 
1. Go to **Machine Manager → Configuration → Machine Model** and create
   the model types relevant to your business (e.g. vehicle types, equipment
   categories).
 
2. Open any product in Odoo and enable the **"Can be a Machine"** option
   to make it available for linking to machine records.
 
3. Go to **Machine Manager → Configuration → Machines** and start adding
   your equipment.
 
4. Assign the appropriate roles (**User** or **Manager**) to your team
   members from **Settings → Users**.
   
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
* Daniel Campos <danielcampos@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@serviciobaeza.com>
* Ana Juaristi <ajuaristio@gmail.com>
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Esther Martín <esthermartin@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
