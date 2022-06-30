# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    is_incubator = fields.Boolean(
        string="Incubator", compute="_compute_is_incubator", store=True)

    @api.depends("category_type_id")
    def _compute_is_incubator(self):
        for line in self:
            line.is_incubator = False
            if (
                line.category_type_id) == (
                    self.env.ref("stock_warehouse_farm.categ_type6")):
                line.is_incubator = True
