.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
L10n es deca oca origin
========================

DECA Transport Management
=========================

This module extends the Spanish DECA functionality to manage transport
operations from sales orders to delivery orders and customer invoices.

Main Features
-------------

* Import DECA sales orders from Excel files.
* Automatically create sales orders and order lines from imported data.
* Identify customers, carriers, loading locations and delivery locations.
* Manage tractor and trailer vehicles and their licence plates.
* Manage transport information, including loading dates, cargo weights,
  occupation, special traffic authorisations and DECA notes.
* Transfer DECA information from sales orders to stock pickings and invoices.
* Generate DECA transport reports directly from completed stock pickings.
* Validate mandatory DECA information before confirming sales orders
  and generating transport reports.
* Check mandatory identification numbers (VAT/NIF) for carriers,
  senders and consignees.
* Manage transport-specific information throughout the sales,
  stock and accounting workflows.

The module is designed to facilitate the management of DECA transport
documentation and integrate transport information into the standard
Odoo sales, inventory and accounting processes.

Usage
-----

* In Sales - Configuration, new menu option "Import DECA Sale Orders".
* The "Loading location" and "Delivery location" data are entered into
  the sales order lines.
* The DECA report is generated from the picking.
* The DECA information from the sales order is also carried over to the
  invoice.

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
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
