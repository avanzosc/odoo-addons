.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Stock Quant Create Fix
======================

When setting package or owner on outgoing stock move line odoo core creates always a new quant with negative quantities, but if there is an existing quant without owner or package, the new quant shouldn't be created only the quantities on existing quant should be created.
Core is working with lot but no with package and owners so, this is a fix.

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
