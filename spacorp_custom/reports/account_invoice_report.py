# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_shipping_id = fields.Many2one(
        string="Shipping address", comodel_name="res.partner", readonly=True
    )
    city = fields.Char(string="City", readonly=True)
    state_id = fields.Many2one(
        string="Province", comodel_name="res.country.state", readonly=True
    )
    shipping_city = fields.Char(string="Shipping city", readonly=True)
    shipping_state_id = fields.Many2one(
        string="Shipping province", comodel_name="res.country.state", readonly=True
    )

    def _select(self):
        select = super()._select()
        select = (
            "{}, move.partner_shipping_id as partner_shipping_id, "
            "move.shipping_city as shipping_city, "
            "move.shipping_state_id as shipping_state_id, "
            "move.city as city, "
            "move.state_id as state_id "
        ).format(select)
        return select
