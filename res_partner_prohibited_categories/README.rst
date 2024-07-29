.. image:: https://img.shields.io/badge/license-AGPL-3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=================================
Res Partner Prohibited Categories
=================================

This module enhances the functionality of Odoo by allowing the management of prohibited product categories for partners. It ensures that customers cannot see or purchase products belonging to prohibited categories assigned to them or their designated pick-up points.

Functionality
-------------

- **Prohibited Product Categories for Partners**: Partners (customers) can have product categories that are prohibited for them. This is managed through a Many2many field on the partner form.

- **Related Prohibited Product Categories**: When a partner has a designated pick-up point, the prohibited categories of the pick-up point are also applied to the partner. This is managed through a computed Many2many field that aggregates the prohibited categories from the pick-up point.

- **Product Filtering in Website**: When a logged-in customer browses the online store, products that belong to their prohibited categories (either directly assigned or inherited from their pick-up point) are filtered out and not displayed.


Contributions
-------------

- Bug reports and feature requests can be submitted on `GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`.
- Contributions to the codebase are welcome via pull requests.

Credits
=======

Contributors
------------

* Unai Beristain <unaiberistain@avanzosc.es>