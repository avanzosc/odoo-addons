
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    is_fsc_certificate = fields.Boolean(
        'Contains FSC certificate', compute="_compute_contains_fsc_products", store=True)

    def _compute_contains_fsc_products(self):
        for record in self:
            certificates = record.invoice_line_ids.mapped('product_id').mapped('is_fsc_certificate')
            record.is_fsc_certificate = (True in certificates)

    def recalc_fsc_certificated(self):
        self._compute_contains_fsc_products()
