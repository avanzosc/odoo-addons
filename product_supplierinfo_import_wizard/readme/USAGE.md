To use this module, you need to be in the *Settings / Technical* group
(since access is restricted to `base.group_system`).

1. Go to *Settings > Technical > Import > Import Supplier Pricelists*.

2. Click **Create** and fill in the following:
   - **Data**: Upload your CSV file with the supplier pricelist data.
   - **Company**: Select the company for which the pricelist applies
     (defaults to your current company).

3. The CSV file must contain the following column headers (in Spanish):

   - `Proveedor` — supplier name
   - `Código de producto` — product internal reference
   - `Plantilla de producto` — product name
   - `Nombre del producto del proveedor` — vendor product name
   - `Código de producto del proveedor` — vendor product code
   - `Precio` — purchase price
   - `Moneda` — currency ISO code (e.g., EUR, USD)
   - `Secuencia` — sequence (priority)
   - `Cantidad mínima` — minimum quantity
   - `Fecha de inicio` — start date
   - `Fecha finalización` — end date
   - `Tiempo inicial entrega` — delivery lead time (days)

4. Click **Import** to parse the file and create the import lines.

5. Click **Validate** to check that suppliers, products, and currencies
   exist in the database. Lines with errors will be highlighted in red
   with a description of the problem.

6. If needed, edit lines directly in the editable tree view to fix any
   validation errors (e.g., select the correct supplier or product manually).

7. Click **Process** to create the `product.supplierinfo` records for all
   valid lines.

8. Use the **Supplier Infos** stat button to review the newly created
   supplier pricelist records.
