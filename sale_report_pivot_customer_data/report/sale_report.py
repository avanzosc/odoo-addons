# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_state_id = fields.Many2one(comodel_name="res.country.state", string="State")
    partner_city = fields.Char(string="City")
    partner_shipping_state_id = fields.Many2one(
        comodel_name="res.country.state", string="Shipping province"
    )
    partner_shipping_city = fields.Char(string="Shipping city")
    order_partner_shipping_id = fields.Many2one(
        string="Shipping address", comodel_name="res.partner"
    )

    def _select(self):
        res = super()._select()
        res += (
            ", l.order_partner_shipping_id as order_partner_shipping_id"
            ", l.partner_state_id as partner_state_id"
            ", l.partner_city as partner_city"
            ", l.partner_shipping_state_id as partner_shipping_state_id"
            ", l.partner_shipping_city as partner_shipping_city"
        )
        return res

    def _group_by(self):
        res = super()._group_by()
        res += (
            ", l.order_partner_shipping_id"
            ", l.partner_state_id"
            ", l.partner_city"
            ", l.partner_shipping_state_id"
            ", l.partner_shipping_city"
        )
        return res
