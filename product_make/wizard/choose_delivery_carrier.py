# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = "choose.delivery.carrier"

    make_id = fields.Many2one(string="Make", comodel_name="product.make")

    @api.depends("partner_id")
    def _compute_available_carrier(self):
        result = super()._compute_available_carrier()
        for rec in self:
            make = rec.make_id
            rec.available_carrier_ids = rec.available_carrier_ids.filtered(
                lambda c, make=make: make
                in c.product_id.product_tmpl_id.product_make_ids
            )
        return result
