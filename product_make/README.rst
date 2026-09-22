.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Product make
============

* Nuevo objeto "Marcas", el mantenimiento de este objeto se hace desde
  Ventas - Configuración - Productos.
* A un producto se le podrán asignar varias "Marcas".
* En cliente nueva relacion a nueva tabla "Marcas-Comercial". Esta nueva tabla
  tiene los campos Marca y comercial. Por defecto, al añadir una línea en la
  tabla, el campo comercial será informado con el dato de comercial de la ficha
  del cliente, aunque el usuario podrá poner otro comercial diferente del de su
  ficha.
* Añadir relación a MARCA en la línea de pedido de venta. Este campo será
    obligatorio, solo se podrán seleccionar marcas asociadas al producto, y se
    calculará de la siguiente forma:
** Si el producto tiene asignada una sola marca, se cogerá esta marca.
** Si el producto tiene asignada mas de una marca, por cada marca iremos a la
   nueva tabla "Marcas-Comercial" del cliente, Si no se encuentran líneas o da
   más de una, el usuario pondrá el dato a mano.
** Todo lo relacionado con la marca en el pedido de venta, se llevará también
   a albaranes, y facturas.


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

* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
