.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=================================================
Account invoice supplier ref unique by fiscalyear
=================================================

* This module checks that a supplier invoice/refund is not entered twice for
  the same fiscal year. This is important because if you enter twice the
  same supplier invoice, there is also a risk that you pay it twice !

* This module adds a constraint on supplier invoice/refunds to check that
  (commercial_partner_id, supplier_invoice_number, fiscal year) is unique,
  without considering the case of the supplier invoice number.

Credits
=======


Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
