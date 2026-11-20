# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    product_length = fields.Float(string="Length", digits="Product Unit of Measure")
    product_height = fields.Float(string="Height", digits="Product Unit of Measure")
    product_width = fields.Float(string="Width", digits="Product Unit of Measure")
    dimensional_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )
    product_weight = fields.Float(string="Weight", digits="Stock Weight")

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for lot in self:
            lot.volume = template_obj._calc_volume(
                lot.product_length,
                lot.product_height,
                lot.product_width,
                lot.dimensional_uom_id,
            )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]
