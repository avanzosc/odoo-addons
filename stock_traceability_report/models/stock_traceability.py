from odoo import api, models


class MrpStockReport(models.TransientModel):
    _inherit = "stock.traceability.report"

    @api.model
    def _final_vals_to_lines(self, final_vals, level):
        lines = super()._final_vals_to_lines(final_vals, level)
        for key, data in enumerate(final_vals):
            lines[key].get("columns").append(data.get("partner_id", ""))
        return lines

    def _make_dict_move(self, level, parent_id, move_line, unfoldable=False):
        res = super()._make_dict_move(level, parent_id, move_line, unfoldable)
        if move_line.move_id.picking_id and move_line.move_id.picking_id.partner_id:
            res[0].update(
                {
                    "partner_id": move_line.move_id.picking_id.partner_id.display_name,
                }
            )
        return res
