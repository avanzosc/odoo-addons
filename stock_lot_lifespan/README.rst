.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Stock Lot Lifespan
==================

* Lifespan in Lots. The lifespan is the difference between 'Mrp Date' and 'Life
  Date' in the lot and is measured in days.
* Three new alert percentage fields in Warehouse Configuration. There, you
  must define lifespan percentage in which you want to be notified.
* 'Alert Date', 'Removal Date' and 'Use Date' are renamed as 'Lifespan 1st Alert',
  'Lifespan 2nd Alert' and 'Lifespan 3rd Alert' respectively. These one are
  calculated by percentages defined in the configuation when any of 'Mrp Date' and
  'Life Date' fields are modified.
* When the module is installed, the alert fields in lots are updated if mrp and
  life dates are filled.
* Create an email to notify which lots have exceeded the lifespan today.
* New automated action to send the previous email once per day.

Credits
=======


Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
