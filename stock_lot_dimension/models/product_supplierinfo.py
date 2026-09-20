# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]

    purchase_weight = fields.Float(string="Teorical Weight")
    purchase_weight_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        default=lambda self: self.env[
            "product.template"
        ]._get_weight_uom_id_from_ir_config_parameter(),
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_kgm").id)
        ],
    )
    purchase_length = fields.Float()
    purchase_length_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        default=lambda self: self.env.ref("uom.product_uom_cm"),
        domain=lambda self: self._get_dimension_uom_domain(),
    )

    @api.onchange("product_id", "product_tmpl_id")
    def onchange_product_id(self):
        if self.product_id:
            self.purchase_weight = self.product_id.weight
            self.purchase_length = self.product_id.product_length
        elif self.product_tmpl_id:
            self.purchase_weight = self.product_tmpl_id.weight
            self.purchase_length = self.product_tmpl_id.product_length
