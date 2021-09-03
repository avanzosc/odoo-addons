# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(
        search="_search_product_pricelist")

    @api.model
    def _search_product_pricelist(self, operator, value):
        result = self.env["ir.property"].search_multi(
            "property_product_pricelist", "res.partner", operator, value)
        return result
