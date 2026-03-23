.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Machine manager product manufacturer
====================================

A new read-only **Manufacturer** field is added to every machine record,
visible in the **Manufacture Details** section of the **Additional Details**
tab. The value is taken automatically from the manufacturer defined on the
product linked to the machine.
 
Since the field is a stored related field, it always stays in sync with
the product — if you update the manufacturer on the product, the machine
record reflects the change automatically without any manual intervention.
 
Manufacturer Column in the Machine List
-----------------------------------------
 
In the machine list view, a new optional column **Manufacturer** is
available. When enabled, it shows the manufacturer of each machine at a
glance, making it easy to filter and compare equipment from different
suppliers without opening individual records.
 
Search and Group Machines by Manufacturer
-------------------------------------------
 
The machine search view includes a new **Manufacturer** filter. You can
search for machines by manufacturer name directly from the search bar.
 
A new **Manufacturer** option is also available in the **Group By** menu,
allowing you to group your entire machine registry by manufacturer for a
quick overview of your equipment fleet by brand or supplier.
 
How It Works
============
 
The manufacturer information lives on the product catalogue, managed by
the **Product Manufacturer** module. This module simply surfaces that
information on the machine record through a related field — there is no
duplication of data and no additional configuration required.
 
The workflow is:
 
1. Assign a manufacturer to a product in the product catalogue.
2. Link that product to a machine in Machine Manager.
3. The **Manufacturer** field on the machine is populated automatically.
 
Configuration
=============
 
No configuration is required. Simply ensure that:
 
1. The **Product Manufacturer** module is installed and manufacturers are
   assigned to your products.
2. Each machine has an **Associated Product** selected in its record.
 
The manufacturer will appear automatically on the machine once both
conditions are met.

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
