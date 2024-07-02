# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _compute_customer_product_code(self):
        for move in self:
            product_code = ""
            if (
                move.product_id
                and move.product_id.customer_code_ids
                and move.picking_id.partner_id
            ):
                partner = (
                    move.picking_id.partner_id
                    if not move.picking_id.partner_id.parent_id
                    else move.picking_id.partner_id.parent_id
                )
                lines = move.product_id.customer_code_ids.filtered(
                    lambda x: x.partner_id == partner
                )
                if lines:
                    for line in lines:
                        product_code = line.customer_code
            move.customer_product_code = product_code

    def _compute_product_display_name(self):
        for move in self:
            product_display_name = move.product_id.display_name
            if (
                move.picking_id.picking_type_id.code == "outgoing"
                and move.product_id.default_code
                and move.customer_product_code
                and move.product_id.default_code in product_display_name
            ):
                new_value = product_display_name.replace(
                    move.product_id.default_code, move.customer_product_code
                )
                product_display_name = new_value
            move.product_display_name = product_display_name

    customer_product_code = fields.Char(
        string="Customer product code", compute="_compute_customer_product_code"
    )
    product_display_name = fields.Char(
        string="Product display name", compute="_compute_product_display_name"
    )
