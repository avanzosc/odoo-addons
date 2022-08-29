# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_name_to_print = fields.Char(
        string="Product name to print",
        compute="_compute_product_name_to_print")

    def _compute_product_name_to_print(self):
        for move in self:
            name = move.product_id.name
            if move.product_id.default_code:
                name = "[{}] {}".format(
                    move.product_id.default_code, move.product_id.name)
            if move.product_customer_code:
                name = "[{}] {}".format(
                    move.product_customer_code, move.product_id.name)
            move.product_name_to_print = name
