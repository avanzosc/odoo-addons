.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Stock Move Line Package Group
=============================

This module decouples the visibility of package fields in Stock Move Lines from the standard Odoo inventory groups.

It introduces a dedicated security group that controls whether users can view the source package and destination package fields in stock move line operations, independently of the default stock permissions.

Features
--------

* New security group `See packages in Stock Move Lines`.
* Independent control of package visibility without relying on standard Inventory groups.
* Controls visibility of:

  * Source Package (`package_id`)
  * Destination Package (`result_package_id`)
* Applies to all major Stock Move Line views:

  * Detailed Operations Tree View
  * Operations Tree View
  * Batch Picking Move Lines View
  * Stock Move Line Form View
* Allows administrators to grant package visibility only to specific users.

Security
--------

**Group:** `group_stock_move_line_package`

Users assigned to this group can view package-related fields in Stock Move Lines.

Users without this group will not see the package fields, regardless of their membership in other stock-related groups.

Technical Details
-----------------

The module adds a new security group and updates the corresponding stock move line views by assigning group-based visibility to the following fields:

* `package_id`
* `result_package_id`

This provides a simple and maintainable way to manage package visibility independently from Odoo's standard inventory security configuration.


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
* Ana Juaristi <ajuaristio@gmail.com>
* Berezi Amubieta <bereziamubieta@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
