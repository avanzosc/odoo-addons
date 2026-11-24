.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

========================
Stock Partner Daily Mail
========================

* Adds the "Send Stock by Email" check to the contact form, next to the tags,
  and a filter with the same name in the contacts search view.
* A daily scheduled action "Contacts: Send Daily Stock" sends an email to every
  contact with the check marked and an email address. The scheduled action is
  created inactive, planned at 13:00 (Europe/Madrid).
* After every run, the next execution is planned for the same local time of the
  next day, also when the daylight saving time changes. The time zone is the
  one of the user of the scheduled action, or Europe/Madrid if it has none.
* The emails are sent at once, without waiting for the outgoing mail queue.
* The email uses the template "Contact: Daily Stock", in the language of the
  contact, and attaches the Excel file ``stock_YYYY_MM_DD.xlsx``.
* The Excel file lists the active product variants that can be sold, can be
  purchased and are published on the website, with these columns: Reference,
  Product, Sale Price, Barcode, Brand and Stock. Stock is the free quantity
  (on hand minus reserved); negative values are shown as 0.
* The column headers of the Excel file are in the language of the contact. The
  product names are always in English.
* Every time the scheduled action runs, the file is generated once per installed
  language and used for all the recipients with that language. Contacts whose
  language is not installed receive the English file.
* The files are also saved on the server, even if no contact has the check
  marked, in the folder ``export_stock/<database>`` inside the Odoo data
  directory, as ``stock_YYYY_MM_DD_<language>.xlsx``. Files older than 15 days
  are deleted from that folder.
* The emails are kept once they have been sent, together with their attached
  file, and are shown in the history of the contact.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/odoo-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
