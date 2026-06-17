.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Product Pricelist Item Menu
===========================

This module extends the functionality of **Contacts** and **Pricelists** in Odoo.  
It allows users to view and directly access the pricelist items related to a specific partner, improving usability and visibility for sales managers.

Key Features
============

- Adds a **stat button** on the partner form to display the number of pricelist items linked to the partner’s assigned pricelist.  
- Provides a direct shortcut to open and review the corresponding **pricelist items**.  
- Enhances the `product.pricelist.item` tree view by showing additional optional fields such as:
  - Base
  - Price Discount
  - Applied On
  - Compute Price  
- Extends the search view for pricelist items with useful filters and grouping options:
  - Group by Pricelist, Base, Apply On, Compute Price
  - Group by Product, Product Template, Product Category, Other Pricelist  
- Adds a dedicated menu entry **Pricelist Items** under *Sales > Products* (visible only to Sales Managers).

Usage
=====

1. Go to **Contacts** and open a partner.  
2. In partners, a stat button **Pricelist Items** will be displayed.  
3. Clicking this button will open the corresponding pricelist items in list and form views.  
4. Alternatively, Sales Managers can access all pricelist items from the **Sales > Products > Pricelist Items** menu.  

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
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
