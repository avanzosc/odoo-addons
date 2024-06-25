# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    is_incubator = fields.Boolean(
        string="Incubator", compute="_compute_type", store=True
    )
    is_integration = fields.Boolean(
        string="Integration", compute="_compute_type", store=True
    )
    is_reproductor = fields.Boolean(
        string="Reproductor", compute="_compute_type", store=True
    )
    is_feed_flour = fields.Boolean(
        string="Feed/Flour", compute="_compute_type", store=True
    )
    is_medicine = fields.Boolean(string="Medicine", compute="_compute_type", store=True)

    @api.depends("type_id")
    def _compute_type(self):
        for line in self:
            is_incubator = False
            is_integration = False
            is_reproductor = False
            is_feed_flour = False
            is_medicine = False
            if (line.type_id) == (self.env.ref("stock_warehouse_farm.categ_type1")):
                is_reproductor = True
            if (line.type_id) == (self.env.ref("stock_warehouse_farm.categ_type2")):
                is_integration = True
            if (line.type_id) == (self.env.ref("stock_warehouse_farm.categ_type3")):
                is_medicine = True
            if (line.type_id) in (
                self.env.ref("stock_warehouse_farm.categ_type4"),
                self.env.ref("stock_warehouse_farm.categ_type5"),
            ):
                is_feed_flour = True
            if (line.type_id) == (self.env.ref("stock_warehouse_farm.categ_type6")):
                is_incubator = True
            line.is_incubator = is_incubator
            line.is_integration = is_integration
            line.is_reproductor = is_reproductor
            line.is_feed_flour = is_feed_flour
            line.is_medicine = is_medicine
