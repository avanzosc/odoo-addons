.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Contacts School
===============

* New object "Partner information type".
* New object "Partner information".
* New relationship of partners to new object "Student characteristic".
* In partner object, new field "Educational category".
* New relationship of partners to partners of category "association",
  "federation". partners with educational category "School" will necessarily
  have at least one category line "association", and another category
  "federation".
* In partner object, family sequence: Each time a family is registered, it
  should be numbered with a customized sequential.
* In partner object, new field "gender", with the values "male" and "female",
  which should only be visible in partners with educational category "Student",
  "Progenitor", "Legal guardian" or "Other children".
* In partner object, new field "old student".
* In partner object, of type "Student", new object "Student payers".

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
