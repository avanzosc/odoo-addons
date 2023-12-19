# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_create_invoice(self):
        result = super(PurchaseOrder, self.with_context(
            from_purchase_order=True)).action_create_invoice()
        self.sudo()._read(['invoice_ids'])
        invoices = self.invoice_ids
        for invoice in invoices:
            invoice.put_notes_from_purchase_order()
        return result
