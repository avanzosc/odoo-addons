from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    total_weight_qty = fields.Float(compute="_compute_picking_ids", store=True)

    @api.depends("invoice_line_ids", "invoice_line_ids.total_weight_qty")
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.total_weight_qty = sum(
                invoice.invoice_line_ids.mapped("total_weight_qty")
            )
