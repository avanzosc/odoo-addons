# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    with_origin_global_gap = fields.Boolean(
        string="With Origin/Global Gap",
        compute="_compute_with_origin_global_gap")

    def _compute_with_origin_global_gap(self):
        for invoice in self:
            with_origin_global_gap = False
            if invoice.move_type == "out_invoice":
                lines = invoice._get_invoiced_lot_values()
                if lines:
                    for line in lines:
                        if "lot_id" in line and line.get("lot_id", False):
                            lot = self.env["stock.lot"].browse(
                                line.get("lot_id"))
                            product = lot.product_id
                            if product.show_origin_global_gap_in_documents:
                                with_origin_global_gap = True
            invoice.with_origin_global_gap = with_origin_global_gap
