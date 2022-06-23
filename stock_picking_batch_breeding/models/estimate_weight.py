# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EstimateWeight(models.Model):
    _name = "estimate.weight"
    _description = "Estimate Weight"

    def _get_default_weight_uom(self):
        try:
            return self.env.ref("uom.product_uom_gram").id
        except Exception:
            return False

    day = fields.Integer(string='Day')
    estimate_weight = fields.Float(string='Estimate Weight')
    estimate_week_weight = fields.Float(string='Estimate Week Weight')
    real_weight = fields.Float(string='Real Weight')
    weight_uom_id = fields.Many2one(
        string="Weight UOM",
        comodel_name="uom.uom",
        default=_get_default_weight_uom,
        domain=lambda self: [
            ("category_id", "=",
             self.env.ref("uom.product_uom_categ_kgm").id)])
    batch_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    date = fields.Date(string="Date")
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
        store=True)
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="batch_id.warehouse_id",
        store=True)
    farmer_id = fields.Many2one(
        string="Farmer",
        comodel_name="res.partner",
        related="warehouse_id.farmer_id",
        store=True)
