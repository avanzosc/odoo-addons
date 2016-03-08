.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Event calendar holiday
======================

* This module allows you to associate holiday calendars, to the contracts
  associated with sales orders.
* By confirming the sales order, and generate the event's sessions, if the date
  of the session coincides with a day of holiday calendars defined in the sale
  contract, the "absence type" field defined in date calendar holidays, it will
  take to the session.
* The field "type of absence" is also defined in the model "presence" of the
  sessions.
* When an employee is added to an event/session, it will take the "type of
  absence" from the session object, to the field "type of absence" of the
  object "presence".

Configuration
=============

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>