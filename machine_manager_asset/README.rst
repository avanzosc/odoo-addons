.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Machine manager asset
=====================

Machine Manager Asset is a companion module for **Machine Manager** that
completes the accounting traceability of your machinery by automatically
linking each machine to its corresponding **fixed asset** record. It
connects the asset generated during invoice validation directly to the
machine that was created when the equipment was received.
 
This module requires **Machine Manager** and the **Asset Management**
(`account_asset_management`) OCA module to be installed. Once both are
present, this module activates automatically.
 
Features
========
 
Automatic Asset Linking on Invoice Validation
-----------------------------------------------
 
When a vendor bill is validated and it generates a fixed asset for a
product marked as **"Can be a Machine"**, the module automatically finds
the machine that was created from that purchase and links the asset to it.
 
For the automatic linking to work, the invoice line must have:
 
- A product marked as **"Can be a Machine"**
- An **Asset Profile** assigned to the invoice line with the option
  **Asset per product item** enabled
- A generated asset on the line
- A linked purchase order line
 
The matching is done by tracing back from the invoice line through the
purchase line to the stock move lines, matching by serial number when
available to ensure the correct machine is identified in multi-unit
purchases.
 
Asset Field on the Machine Record
-----------------------------------
 
A new **Asset** field is added to every machine record, visible in the
**Financial Details** tab alongside the other financial information.
It links directly to the fixed asset record in the asset management
module, giving you one-click navigation from the machine to its
depreciation schedule, asset value, and accounting entries.
 
The field can also be set manually if needed, for example to link
machines that were registered before this module was installed.
 
Asset Column in the Machine List
----------------------------------
 
In the machine list view, a new optional column **Asset** is available.
When enabled, it shows the linked asset for each machine at a glance,
making it easy to identify which machines have been registered as fixed
assets and which have not.
 
Search and Group Machines by Asset
------------------------------------
 
The machine search view includes a new **Asset** filter. You can search
for machines by asset name or reference directly from the search bar.
 
A new **Asset** option is also available in the **Group By** menu,
allowing you to group your machine registry by asset for accounting
and audit purposes.
 
Configuration
=============
 
No additional configuration is required beyond the base modules. The
only prerequisite is:
 
1. When creating the vendor bill for a machine purchase, assign an
   **Asset Profile** with **Asset per product item** enabled directly
   on the invoice line of the machine product.
 
2. Validate the invoice. The asset is created by `account_asset_management`
   and this module links it to the corresponding machine automatically.

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
