.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Machine Manager Purchase Account
================================

Machine Manager Purchase Account is a companion module for **Machine Manager
Purchase** that completes the financial traceability of your machinery by
linking each machine to its **purchase invoice**. It extends the acquisition
chain that was already established by Machine Manager Purchase, adding the
final accounting step:
 
.. code-block::
 
   Purchase Order → Incoming Shipment → Machine Created → Purchase Invoice linked
 
This module requires **Machine Manager Purchase** and the **Accounting**
module to be installed. Once both are present, this module activates
automatically.
 
Features
========
 
Automatic Invoice Linking on Validation
-----------------------------------------
 
When a **vendor bill** (purchase invoice) is validated, the module
automatically finds all machines that were created from the related purchase
order and links the invoice to them.
 
The matching is done by comparing the invoice origin reference with the
purchase order name.
 
Purchase Invoice on the Machine Record
----------------------------------------
 
A new **Purchase Invoice** field is added to every machine record, visible
in the **Financial Details** tab alongside the other purchase information
already provided by Machine Manager Purchase.
 
Quick Access from the Vendor Bill
-----------------------------------
 
A smart button on the **Vendor Bill** form shows how many machines are
linked to that invoice. Clicking it opens the filtered list of those
machines directly, giving accounting staff instant visibility of which
assets correspond to each invoice without leaving the accounting module.
 
The button only appears once at least one machine is linked to the invoice,
and is only visible to users with the **Machine Management** role.
 
Search and Group Machines by Invoice
--------------------------------------
 
The machine list and search view include an additional filter and grouping
option based on the purchase invoice:
 
- Search machines by **Purchase Invoice**.
- Group machines by **Purchase Invoice** for a quick overview of which
  assets were acquired in each billing cycle.
 
The Purchase Invoice is also available as an optional column in the machine
list view.
 
Configuration
=============
 
No additional configuration is required. The module works automatically
once installed:
 
1. Machines are created automatically when a purchase receipt is validated
   (handled by **Machine Manager Purchase**).
 
2. When the corresponding vendor bill is validated in Accounting, the
   module finds all machines from that purchase order and links the invoice
   to them automatically.
 
3. The smart button on the vendor bill and the Purchase Invoice field on
   the machine record are immediately available to users with the
   **Machine Management / User** role or higher.

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
