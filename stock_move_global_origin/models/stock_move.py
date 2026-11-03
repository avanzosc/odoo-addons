# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_type_sequence_code = fields.Char(
        string="Operation Code", related="picking_type_id.sequence_code", store=True
    )

    global_origin = fields.Char(
        compute="_compute_global_origin", store=True, index=True, recursive=True
    )

    @api.depends(
        "sale_line_id.order_id.global_origin",
        "purchase_line_id.order_id.global_origin",
        "raw_material_production_id.global_origin",
        "production_id.global_origin",
        "move_dest_ids.global_origin",
        "move_orig_ids.global_origin",
    )
    def _compute_global_origin(self):
        for move in self:
            document = move._get_global_origin_document()
            if document:
                origins = document.mapped("global_origin")
            elif move._is_global_origin_demand():
                origins = move.move_dest_ids.filtered(
                    lambda dest: dest._is_global_origin_demand()
                ).mapped("global_origin")
            else:
                origins = move._get_upstream_global_origins()
            move.global_origin = next((origin for origin in origins if origin), False)

    def _get_global_origin_document(self):
        self.ensure_one()
        return (
            self.sale_line_id.order_id
            or self.purchase_line_id.order_id
            or self.raw_material_production_id
            or self.production_id
        )

    def _is_global_origin_demand(self):
        # Purchases, productions and the moves before them only read moves that
        # lead to a document. Otherwise a step that nothing demands, which takes
        # its origin from the moves before it, would close a loop
        self.ensure_one()
        seen = self.browse()
        moves = self
        while moves:
            if any(move._get_global_origin_document() for move in moves):
                return True
            seen |= moves
            moves = moves.move_dest_ids - seen
        return False

    def _get_upstream_global_origins(self):
        self.ensure_one()
        seen = self
        moves = self.move_orig_ids
        while moves:
            seen |= moves
            documented = moves.filtered(lambda move: move._get_global_origin_document())
            origins = documented.mapped("global_origin")
            if any(origins):
                return origins
            moves = (moves - documented).move_orig_ids - seen
        return []
