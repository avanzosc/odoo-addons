from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def validate_and_send_invoice(self, auto_commit, invoice):
        pass

    @api.model
    def _cron_recurring_create_invoice(self):
        return self._create_recurring_invoice(automatic=False)
