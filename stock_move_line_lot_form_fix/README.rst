.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

============================
Stock Move Line Lot Form Fix
============================

This module fixes the default Odoo behavior when clicking **"Create and Edit"** on 
the **lot_id** field in **stock.move.line** (picking operations).

By default, Odoo opens a **simplified minimal form** for the Lot/Serial Number, 
which **doesn't include important fields like expiration dates, best before date, alert date, etc**.

With this module:

* Odoo will **force the full production lot form view** (``stock.view_production_lot_form``) 
when creating or editing a lot from a picking.
* This ensures that users can enter data like **Expiration Date**, 
**Best Before Date**, **Alert Date**, **Removal Date**, and other custom fields.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_.  
In case of trouble, please check there if your issue has already been reported.  
If not, help us by creating a new detailed issue.

**Do not contact contributors directly for support or help with technical issues.**

Credits
=======

Contributors
------------

* Ane Gurruchaga <aneavanzosc@gmail.com>
* Ana Juaristi <anajuaristi@avanzosc.es>