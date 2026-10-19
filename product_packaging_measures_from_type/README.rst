.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

====================================
Product Packaging Measures From Type
====================================

This module calculates the gross weight and height of product packagings
from the dimensions of their package type, and detects when a packaging
is a pallet built from smaller packagings of the same product.

It builds on top of ``product_packaging_is_pallet`` and
``product_packaging_dimension``, reusing the ``weight``/``height``/
``is_pallet`` fields on ``product.packaging`` that those modules already
provide, instead of redefining them.

**Features**

- **New field on Package Types (stock.package.type)**

  - ``qty_per_layer``: number of packages of this type that fit in a
    single layer when stacked on a pallet. Defaults to 1. Used to estimate
    the height of a pallet from the number of inner packages it contains.

- **Product Packaging (product.packaging)**

  - ``package_type_id`` is now required.
  - ``is_pallet`` (added by ``product_packaging_is_pallet`` as a manual
    checkbox) is now set automatically by the recalculation below instead.

- **Recalculate Packaging Weight and Height** (``product.product``)

  - Server action available on one or several products.
  - For every ``product.packaging`` of the product (from smallest to
    largest quantity), calculates the gross weight from the product's net
    weight plus the empty weight of its package type.
  - When a packaging is found to contain an exact number of a smaller
    packaging (e.g. a pallet built from boxes), it is flagged as a pallet:
    the weight also adds the empty weight of every inner packaging, and
    the height is estimated from the number of layers
    (``qty_per_layer``) of the inner packaging.
  - Runs automatically whenever the product's ``weight`` changes, or a
    ``product.packaging`` of the product has its ``package_type_id`` or
    ``qty`` changed.

- **Data integrity**

  - ``package_type_id`` is now required on ``product.packaging``.
  - ``base_weight``, ``height``, ``width`` and ``packaging_length`` are
    now required to be strictly greater than zero on
    ``stock.package.type``.

Bug Tracker
===========

Bugs are tracked internally for this client's development. In case of
trouble, please contact the contributors below.

Credits
=======

Contributors
------------

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

License
=======

This project is licensed under the AGPL-3 License. For more details, refer
to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
