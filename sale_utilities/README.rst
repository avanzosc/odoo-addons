.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Sale utilities
==============

* The "name_search" function of the "res.partner" model has been changed, to be
  able to search by name, partner_comercial, nif, and reference.

* Group of quotations, and sale orders, by state.

* Group of partners by the first defined label.

* In sales orders, the "terms and conditions" field shows bigger.

* In sales orders, filter shipping and invoicing addresses by partner.

* In sales orders, invoiced and shipped computed fields to new api.
	- Invoiced: When all invoices related to the sale order are in state paid
	this check will be set as True.
	- Shipped: When all pickings related to the sale order are in state done or
	cancel and there is almost one picking in done state, this check will be set
	as True.

* In sales orders tree, invoiced and shipped fields visible.

* New group "View only customers/suppliers of sale person", for view only
  customers and suppliers with saleperson equal to user.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
