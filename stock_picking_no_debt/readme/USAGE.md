To use this module:

1. Go to *Inventory* > *Operations* > *Transfers* and select a delivery picking whose associated sale order has posted but unpaid invoices.
2. The *Pending Sale Invoices* field will be checked on the picking form (next to the *Origin* field).
3. Click **Validate**.
4. A wizard will appear with the message: *"You can not validate picking with pending invoices."*
5. Choose one of the following options:
   - **Apply (no debt)**: Validates all selected pickings EXCEPT those with debt.
   - **Apply**: Validates the pickings that the user has explicitly toggled on, even if they have debt.
   - **Cancel**: Closes the wizard without validating any picking.
6. If the *Show Transfers* option is active (configurable from context), an editable list of affected pickings with individual toggles is displayed to decide which ones to process.
