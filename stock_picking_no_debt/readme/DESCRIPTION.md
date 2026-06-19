This module extends the functionality of delivery pickings (*stock.picking*) to prevent validating pickings whose associated sale orders have pending unpaid invoices.

When a user attempts to validate a picking with posted but unpaid sale invoices, the system displays an informative wizard that allows deciding whether to validate the picking despite the debt, skip the pickings with debt, or cancel the operation. It provides a financial control layer over stock outflows that warns about customers with unpaid invoices without forcibly blocking the operation.
