# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    valued = fields.Boolean(related=False, readonly=False, default=False)

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        result = super().onchange_partner_id()
        for picking in self:
            picking.valued = picking.partner_id.valued_picking
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "partner_id" in vals and vals.get("partner_id", False):
                partner = self.env["res.partner"].browse(vals.get("partner_id"))
                vals["valued"] = partner.valued_picking
        pickings = super().create(vals_list)
        return pickings
