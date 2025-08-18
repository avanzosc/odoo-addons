# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    partner_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        related="order_partner_id.state_id",
        store=True,
    )
    partner_city = fields.Char(
        string="City", related="order_partner_id.city", store=True
    )
    order_partner_shipping_id = fields.Many2one(
        string="Delivery address",
        related="order_id.partner_shipping_id",
        comodel_name="res.partner",
        store=True,
    )
    partner_shipping_state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Delivery address state",
        related="order_partner_shipping_id.state_id",
        store=True,
    )
    partner_shipping_city = fields.Char(
        string="City", related="order_partner_shipping_id.city", store=True
    )
