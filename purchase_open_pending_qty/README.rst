.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
      :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
      :alt: License: AGPL-3

=========================
Purchase Open Pending Qty
=========================

This module is a lightweight wrapper over OCA module ``purchase_open_qty``.
Pending quantities are provided by OCA, and this module keeps only the
project-specific optional line copy action.

Features
========

* Uses ``purchase_open_qty`` as single dependency for:

   * purchase order lines menu
   * pending qty fields (``qty_to_receive`` and ``qty_to_invoice``)
   * standard Odoo received/invoiced qty fields
* Adds optional line copy action button on purchase order lines.

Technical Notes
===============

* Main dependency: ``purchase_open_qty``
* The menu and pending qty logic are provided by OCA module.
* This module does not duplicate OCA pending fields in line views.
* This module only keeps the optional copy-line action.

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
* Aner Arregi <aneravanzosc@gmail.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
