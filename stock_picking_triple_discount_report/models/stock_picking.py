# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    print_discount = fields.Boolean(
        string="Print discount", compute="_compute_print_discounts"
    )
    print_discount2 = fields.Boolean(
        string="Print discount 2", compute="_compute_print_discounts"
    )
    print_discount3 = fields.Boolean(
        string="Print discount 3", compute="_compute_print_discounts"
    )

    def _compute_print_discounts(self):
        for picking in self:
            discount = False
            discount2 = False
            discount3 = False
            lines = picking.move_line_ids.filtered(lambda x: x.sale_discount)
            if lines:
                discount = True
            lines = picking.move_line_ids.filtered(lambda x: x.sale_discount2)
            if lines:
                discount2 = True
            lines = picking.move_line_ids.filtered(lambda x: x.sale_discount3)
            if lines:
                discount3 = True
            picking.print_discount = discount
            picking.print_discount2 = discount2
            picking.print_discount3 = discount3
