# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class GrowthRate(models.Model):
    _name = "growth.rate"
    _description = "Growth Rate"

    def _get_default_weight_uom(self):
        try:
            return self.env.ref("uom.product_uom_gram").id
        except Exception:
            return False

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    day = fields.Integer(string='Day')
    weight = fields.Float(string='Weight')
    weight_uom_id = fields.Many2one(
        string="Weight UOM", default=_get_default_weight_uom,
        comodel_name="uom.uom",
        domain=lambda self: [
            ("category_id", "=",
             self.env.ref("uom.product_uom_categ_kgm").id)])
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
