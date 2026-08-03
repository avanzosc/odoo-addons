============================
Custom Pickings Batch Import
============================

Wizard to import stock.picking.batch records (breeding/mother batches) from
CSV or Excel files.

Models
======

* ``stock.picking.batch.import`` — the import wizard, one per uploaded file.
* ``stock.picking.batch.import.line`` — one line per row read from the file.

Workflow
========

1. Upload a CSV or XLS/XLSX file with the expected columns
   (see the *Help* tab inside the form).
2. Click **Importar** to read the rows into wizard lines.
3. Click **Validar** to resolve references (location, lineage, feed family).
4. Click **Procesar** to create the actual ``stock.picking.batch`` records.

Expected columns
================

* ``Entry Date`` — batch entry date
* ``Type`` — ``mother`` or ``breeding``
* ``Location`` — name or complete_name of a ``stock.location``
* ``Name`` — batch name (must be unique)
* ``Lineage`` — name of a ``lineage`` record
* ``Mother`` — mother batch reference (optional)
* ``Chick Code`` / ``Chick Location`` / ``Chick Lot`` / ``Chick Qty`` — chick
  product movement details
* ``Chicken Code`` / ``Chicken Lot`` / ``Chicken Qty`` — chicken (outgoing)
  product details
* ``Medicine Code`` / ``Medicine Location`` / ``Medicine Qty`` — medicine
  product details
* ``Feed Code`` / ``Feed Location`` / ``Feed Qty`` — feed product details
* ``Feed Family`` — name of a ``breeding.feed`` record

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Aner Arregi <aneravanzosc@gmail.com>
