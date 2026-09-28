.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Account Tax Update OSS
======================

This module adds a server action on Odoo taxes to update OSS-related taxes
with the required fiscal tags for the Spanish localization.

The server action is available from both the tax list and form views. When
executed on a tax whose name contains ``OSS ``, the module updates its Spanish
tax type and adjusts the tags assigned to its repartition lines.

Key features:

* Add an **Update OSS taxes** server action to ``account.tax``.
* Make the server action available from both list and form views.
* Detect OSS taxes by checking whether the tax name contains ``OSS ``.
* Set the Spanish tax type (``l10n_es_type``) to ``no_sujeto_loc``.
* Replace the existing tags on all tax repartition lines with the
  ``l10n_eu_oss.tag_oss`` tag.
* Add the ``+mod303[123]`` tax tag to invoice base repartition lines.
* Support the Spanish localization and EU OSS tax configuration.

Usage / How to test
===================

Backend
-------

1. Go to **Accounting → Configuration → Taxes**.
2. Open an OSS tax or select one or more taxes from the list view.
3. Make sure the tax name contains ``OSS ``, for example
   ``OSS for EU to Alemania: 19.0``.
4. Open the **Action** menu.
5. Click **Update OSS taxes**.
6. Check that the tax field ``l10n_es_type`` has been set to
   ``no_sujeto_loc``.
7. Check the tax repartition lines.
8. Verify that all repartition lines contain the OSS tag from
   ``l10n_eu_oss.tag_oss``.
9. Verify that the invoice base repartition line also contains the
   ``+mod303[123]`` tag.

Taxes whose name does not contain ``OSS `` are not modified by the action.

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
~~~~~~~~~~~~

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
