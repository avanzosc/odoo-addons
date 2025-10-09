.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Stock Ordepoint Usability
=========================

This module improves the usability of **Reordering Rules (Minimum Inventory Rules)** by adding key stock information and quick actions directly in tree and form views.

- Displays the **Name** field in the editable Procurement Order tree view.
- Adds new computed fields to the *Minimum Inventory Rules*:
  - **Quantity On Hand** (`qty_available`)
  - **Incoming** (`incoming_qty`)
  - **Outgoing** (`outgoing_qty`)
  - **Virtual Available** (`virtual_available`)
  - **Forecaster Distinct Forecast** (`forecaster_distinct_forecast`)
- Adds quick action buttons:
  - **Order Once** → create a single replenishment order.
  - **Automate Orders** → enable automatic reordering.
  - **Snooze** → temporarily delay manual rules.
  - **Open Form** → open the orderpoint form view.
  - **Recalculate To Order** → recompute the quantity to order.
- Adds new search filters:
  - *Forecaster distinct forecast*
  - *Forecaster NOT distinct forecast*

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>


Do not contact contributors directly about support or help with technical issues.
