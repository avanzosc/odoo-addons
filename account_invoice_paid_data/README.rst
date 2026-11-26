=========================
Account invoice paid data
=========================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

This module extends the accounting invoices with payment information:

* Adds a paid date field to invoices, filled in automatically when the
  payment state changes to paid.
* Adds a payment period field to invoices, with the number of days between
  the invoice date and the paid date.
* Both fields are shown in the invoices tree view.
* The lines of journal entry templates are copied when the template is
  duplicated.

**Table of contents**

.. contents::
   :local:

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported.

Credits
=======

Authors
~~~~~~~

* Avanzosc

Contributors
~~~~~~~~~~~~

* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
