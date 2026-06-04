from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange("sale_line_id")
    def compute_stock_move_description(self):
        for record in self:
            if record.sale_line_id:
                record.name = record.sale_line_id.name

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves.filtered("sale_line_id").compute_stock_move_description()
        return moves
