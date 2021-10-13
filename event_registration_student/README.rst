.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
Event registration student
==========================

* Student, education center, real date start, date start, real date
  end, and date end in event registration.
* After confirming a sales order, if the sales order lines are associated with
  a contract line, and this sales line is associated with a single event
  registration: the start/end date of the contract line will be the start/end
  date of event registration.
* If the start/end date is changed in the contract line, or in the event
  registration, and if the contract line is associated with a single event
  registration, and a single event registration has a single contract line: if
  it is changed in the participant, they will change on the contract line and
  vice versa.
* When a participant is canceled, or terminated, their contract line is
  terminated.

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
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
