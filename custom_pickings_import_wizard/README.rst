==============================
Custom Pickings Import Wizard
==============================

Wizard to import stock pickings from CSV or Excel files.

Models
======

* ``stock.picking.import`` — the import wizard, one per uploaded file.
* ``stock.picking.import.line`` — one line per row read from the file.

Workflow
========

1. Upload a CSV or XLS/XLSX file with the expected columns
   (see *Help* tab inside the form).
2. Click **Importar** to read the rows into wizard lines.
3. Click **Validar** to resolve references (products, locations, lots,
   carriers, picking types).
4. Click **Procesar** to create the actual ``stock.picking`` records.

Expected columns
================

* ``Fecha`` — picking custom date done
* ``DocumentoOrigen`` — origin document reference
* ``UbicacionOrigen`` — source location name or complete_name
* ``UbicacionDestino`` — destination location name or complete_name
* ``NombreUbicacionDestino`` — partner name (free text)
* ``CodigoProducto`` — product default_code
* ``Mother`` — mother batch name (optional)
* ``DescripcionProducto`` — free-text description
* ``Lote`` — lot name (auto-created if ``lot_create`` checked)
* ``Cantidad`` — quantity
* ``CodigoTransportista`` — delivery.carrier.code
* ``NombreTransportista`` — carrier display name
* ``Matricula`` — license plate
* ``CosteEnvio`` — shipping cost

Multiple rows with the same ``DocumentoOrigen`` and same product are merged
into a single picking with one move and several move lines (one per lot).

Credits
=======

* AvanzOSC <info@avanzosc.es>
