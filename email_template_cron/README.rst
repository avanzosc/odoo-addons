.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Email Template Cron
===================

This module allows scheduling the sending of email templates.

When installing this module a cron job is created to process the email
templates queue, it will send all those templates that have the check "Active
[cron]" set and "Next execution date" is previous than the current. By
default this cron is executed hourly.


Configuration
=============

In order to select which templates are going to be automatically and
periodically sent, user must configure each template by filling some fields:

* Active [cron] must be set True so the configurator in Advanced Settings tab.
* Configurator has 4 fields:
   * Interval number
   * Interval type
   * Next execution date
   * Domain, this will be applied in order to make a selection to the
     applied model.
     **Example**: [('state','=','draft'),('min_date','<',fields.Datetime.now
     ())] in a template applied to stock.picking model will send the email only
     in those pickings that are draft and scheduled date is previous than "now"


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

* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>