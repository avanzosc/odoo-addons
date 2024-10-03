from odoo import api, models


class TicketBAIInvoice(models.Model):
    _inherit = "tbai.invoice"

    def send(self, **kwargs):
        return

    @api.model
    def send_pending_invoices(self):
        return
