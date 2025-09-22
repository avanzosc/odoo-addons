# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model_create_multi  
    def create(self, vals_list):
        picking_obj = self.env["stock.picking"]
        for vals in vals_list:
            if not vals.get("partner_id", False) and vals.get("picking_id", False):
                picking = picking_obj.browse(vals.get("picking_id"))
                vals["partner_id"] = picking.partner_id.id
        return super().create(vals_list)