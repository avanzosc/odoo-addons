# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    location_qty_available = fields.Float(
        string="Quantity On Hand In Location",
        compute="_compute_location_quantities",
        compute_sudo=False,
        digits="Product Unit of Measure",
    )

    @api.depends_context("company", "location", "warehouse")
    def _compute_location_quantities(self):
        res = self.with_context(location_qty_available=True)._compute_quantities_dict()
        for template in self:
            template.location_qty_available = res[template.id]["qty_available"]

    def action_open_quants_real_stock(self):
        return self.with_context(search_default_realstock=True).action_open_quants()
