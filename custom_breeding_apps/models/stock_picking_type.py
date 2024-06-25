# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

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

    @api.depends("category_type_id", "dest_category_type_id")
    def _compute_type(self):
        for line in self:
            is_incubator = False
            is_integration = False
            is_reproductor = False
            is_feed_flour = False
            is_medicine = False
            reproductor = self.env.ref("stock_warehouse_farm.categ_type1")
            integration = self.env.ref("stock_warehouse_farm.categ_type2")
            medicine = self.env.ref("stock_warehouse_farm.categ_type3")
            feed = self.env.ref("stock_warehouse_farm.categ_type4")
            flour = self.env.ref("stock_warehouse_farm.categ_type5")
            incubator = self.env.ref("stock_warehouse_farm.categ_type6")
            if (line.category_type_id == reproductor) or (
                line.dest_category_type_id == reproductor
            ):
                is_reproductor = True
            if (line.category_type_id == integration) or (
                line.dest_category_type_id == integration
            ):
                is_integration = True
            if (line.category_type_id == medicine) or (
                line.dest_category_type_id == medicine
            ):
                is_medicine = True
            if (line.category_type_id in (feed, flour)) or (
                line.dest_category_type_id in (feed, flour)
            ):
                is_feed_flour = True
            if (line.category_type_id == incubator) or (
                line.dest_category_type_id == incubator
            ):
                is_incubator = True
            line.is_reproductor = is_reproductor
            line.is_integration = is_integration
            line.is_medicine = is_medicine
            line.is_feed_flour = is_feed_flour
            line.is_incubator = is_incubator
