.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Machine Manager Purchase
========================

Machine Manager Purchase is a companion module for **Machine Manager** that
connects your machinery records with Odoo's Purchase and Inventory modules.
It automates the creation of machine records when equipment is received
through a purchase order, and enriches each machine with full traceability
back to its origin purchase.
 
This module requires **Machine Manager** and the **Purchase** module with
stock integration (`purchase_stock`) to be installed. Once both are present,
this module activates automatically.
 
Features
========
 
Automatic Machine Creation on Receipt
---------------------------------------
 
When a purchase order containing a product marked as **"Can be a Machine"**
is validated in the incoming shipment, the module **automatically creates a
machine record** for each received unit. No manual intervention is needed.
 
The machine is created with:
 
- A name generated from the purchase order reference, the product's internal
  reference, and the serial number (when available).
- The product linked directly to the machine.
- The serial number assigned during reception.
 
This ensures that every piece of equipment that enters your company through
a purchase is immediately registered in your machine registry, without any
extra steps from the warehouse team.
 
Purchase Information on the Machine Record
-------------------------------------------
 
Every machine created through a purchase automatically displays its full
purchase traceability in the **Financial Details** tab:
 
- **Purchase Order**: the order from which the machine was acquired.
- **Purchase Date**: the date the purchase order was approved.
- **Purchased From**: the supplier who sold the machine.
- **Purchase Value**: the cost of the machine from the purchase line.
- **In Picking**: the incoming shipment through which the machine was received.
 
All these fields are read-only and computed automatically from the linked
purchase data. They update automatically if the purchase information changes.
 
Quick Access from the Purchase Order
--------------------------------------
 
A smart button on the **Purchase Order** form shows how many machines have
been created from that order. Clicking it opens the filtered list of those
machines directly, so purchasing staff can track what equipment has been
registered without leaving the purchase order.
 
The button only appears once at least one machine has been created from
the order.
 
Quick Access from the Incoming Shipment
-----------------------------------------
 
A smart button on the **Incoming Shipment** (receipt) form shows how many
machines were created during that specific reception. Clicking it opens
the filtered list of those machines, giving warehouse staff instant
visibility of what was registered when they validated the receipt.
 
The button only appears once at least one machine has been created from
the shipment.
 
Search and Group Machines by Purchase Data
-------------------------------------------
 
The machine list and search view include additional filters and grouping
options based on purchase information:
 
- Search machines by **Purchase Order**, **Supplier**, **Incoming Shipment**,
  or **Purchase Date**.
- Group machines by **Purchase Order**, **Supplier**, **Incoming Shipment**,
  or **Purchase Date** for quick analysis of your equipment by acquisition.
 
These options are also available as optional columns in the machine list view.
 
Configuration
=============
 
No additional configuration is required beyond the base Machine Manager
setup. The only prerequisite is:
 
1. Mark the relevant serial products as **"Can be a Machine"** in the product form
   (under the general information tab).
 
2. From that point on, any purchase receipt that includes those products
   will automatically generate machine records upon validation.

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
