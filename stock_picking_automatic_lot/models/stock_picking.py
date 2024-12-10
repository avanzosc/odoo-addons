# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tools.float_utils import float_is_zero


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _sanity_check(self, separate_pickings=True):
        precision_digits = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        no_quantities_done_ids = set()
        no_reserved_quantities_ids = set()
        for picking in self:
            if all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits)
                for move_line in picking.move_line_ids.filtered(
                    lambda m: m.state not in ("done", "cancel")
                )
            ):
                no_quantities_done_ids.add(picking.id)
            if all(
                float_is_zero(
                    move_line.reserved_qty,
                    precision_rounding=move_line.product_uom_id.rounding,
                )
                for move_line in picking.move_line_ids
            ):
                no_reserved_quantities_ids.add(picking.id)
        pickings_using_lots = self.filtered(
            lambda p: p.picking_type_id.use_create_lots
            or p.picking_type_id.use_existing_lots
        )
        if pickings_using_lots:
            lines_to_check = pickings_using_lots._get_lot_move_lines_for_sanity_check(
                no_quantities_done_ids, separate_pickings
            )
            for line in lines_to_check:
                if not line.lot_name and not line.lot_id:
                    vals = line._get_value_production_lot()
                    vals["name"] = self.env.ref(
                        "stock.sequence_production_lots"
                    ).next_by_id()
                    line.lot_id = self.env["stock.lot"].create(vals).id
        return super()._sanity_check(separate_pickings=separate_pickings)
