.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Stock Picking Label Print
=========================

New module to printing Batch/Package labels.
- New label data model is created. This model will have all the necesary 
information to print a label. Like the product, product quantity, package type,
package quantity and the batch.
- A new report related to label data is defined in this module.
- In pickings, every transferred line will create a new record of this label
data and it will be related to the origin picking.
- In pickings will be displayed a new button named Print Label, which will print
the records related to the picking.
- There are two level of permissions created. The users in 'Warehouse user' group 
can create label data and can print the reports. And the users in
'Allow modify report data' group will change any value in the label data related to
pickings.


Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

