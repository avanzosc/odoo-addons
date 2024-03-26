
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    is_fsc_certificate = fields.Boolean(
        string="Contains FSC certificate",
        compute="_compute_contains_fsc_products",
        store=True,
    )

    @api.depends(
        "invoice_line_ids", "invoice_line_ids.product_id",
        "invoice_line_ids.product_id.is_fsc_certificate")
    def _compute_contains_fsc_products(self):
        for record in self:
            record.is_fsc_certificate = any(
                record.mapped("invoice_line_ids.product_id.is_fsc_certificate"))
