# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _find_lines_to_put_in_lot_expiration_date(self):
        normal_sale_order_type = self.env.ref(
            "sale_order_type.normal_sale_type")
        lines = super(
            StockPicking, self)._find_lines_to_put_in_lot_expiration_date()
        if lines:
            my_lines = self.env["stock.move.line"]
            for line in lines:
                if not line.sale_line_id:
                    my_lines += line
                if line.sale_line_id and not line.sale_line_id.type_id:
                    my_lines += line
                if (line.sale_line_id and line.sale_line_id.type_id and
                        line.sale_line_id.type_id == normal_sale_order_type):
                    my_lines += line
            lines = my_lines
        return lines
