# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    with_origin_global_gap = fields.Boolean(
        string="With Origin/Global Gap", compute="_compute_with_origin_global_gap"
    )

    def _compute_with_origin_global_gap(self):
        for picking in self:
            with_origin_global_gap = False
            if picking.move_line_ids_without_package:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: x.product_id.show_origin_global_gap_in_documents
                )
                if lines:
                    with_origin_global_gap = True
            picking.with_origin_global_gap = with_origin_global_gap
