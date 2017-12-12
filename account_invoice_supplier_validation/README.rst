.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================================
Account Invoice Supplier Validation
===================================

* This module adds new state in supplier invoices "To Validate". When an
  incoming invoice is confirmed, it will pass to the new state and an email
  will be sent to the manager. Only the managers are able to validate invoices
  in "To Validate" state. After validating the invoice, it is confirmed. The
  rest of the workflow works as usual.

Credits
=======


Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
