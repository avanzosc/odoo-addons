# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    product_id = fields.Many2one(
        index=True
        )
    product_categ_id = fields.Many2one(
        string="Product Category", comodel_name="product.category",
        readonly=True, index=True,
        )
    location_id = fields.Many2one(
        string="Location", comodel_name="stock.location", readonly=True,
        index=True
        )
    location_dest_id = fields.Many2one(
        string="Destination location", comodel_name="stock.location",
        readonly=True, index=True
        )
    not_show_category_in_inventory_reports = fields.Boolean(
        string="NOT show category in inventory reports", readonly=True
        )
    not_show_location_in_inventory_reports = fields.Boolean(
        string="NOT show location in inventory reports", readonly=True
        )

    @api.model
    def create(self, vals):
        layer = super(StockValuationLayer, self).create(vals)
        if layer.stock_move_id:
            layer.put_category_and_locations_info()
        return layer

    def put_category_and_locations_info(self):
        vals = {
            "location_id": self.stock_move_id.location_id.id,
            "location_dest_id": self.stock_move_id.location_dest_id.id
            }
        if self.product_id and self.product_id.categ_id:
            categ = self.product_id.categ_id
            vals.update({
                "product_categ_id": categ.id,
                "not_show_category_in_inventory_reports":
                categ.not_show_in_inventory_reports
                })
        not_show_location = self.put_not_show_in_inventory_reports_info()
        vals["not_show_location_in_inventory_reports"] = not_show_location
        self.write(vals)

    def put_not_show_in_inventory_reports_info(self):
        not_show_location_in_inventory_reports = False
        if (self.stock_move_id.location_id and
                self.stock_move_id.location_id.not_show_in_inventory_reports):
            not_show_location_in_inventory_reports = True
        if self.stock_move_id.location_dest_id:
            ldest = self.stock_move_id.location_dest_id
            if ldest.not_show_in_inventory_reports:
                not_show_location_in_inventory_reports = True
        return not_show_location_in_inventory_reports
