.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====================
Stock Warehouse Farm
====================

This module extends stock and product management with a farm-oriented structure based on sections, product families, and enhanced warehouse data.

It improves traceability across stock operations by adding classification layers and farm-specific operational fields.

Features
--------

- Introduces **Category Type / Section** for classifying products, locations, warehouses, and stock operations.
- Adds **Product Family** for higher-level product grouping.
- Extends products with sections (single and multiple) and family classification.
- Enhances stock locations with section tagging and improved search/display logic.
- Adds origin and destination sections to stock moves, move lines, pickings, and picking types.
- Introduces batch stages with sequencing and batch-type filtering.
- Extends picking batches with farm-related information and stage management.
- Adds extensive farm data to warehouses (capacity, distances, activity, ownership, geolocation, and farm type).
- Improves stock quant traceability with product and location sections.
- Enhances location naming and search with warehouse context.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
