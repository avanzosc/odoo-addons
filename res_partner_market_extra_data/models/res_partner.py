# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_technology_ids = fields.Many2many(
        string="Technologies", comodel_name="res.partner.technology", copy=False
    )
    customer_market_ids = fields.Many2many(
        string="Markets", comodel_name="res.partner.market", copy=False
    )
    customer_state_ids = fields.Many2many(
        string="Customer Statuses",
        comodel_name="res.partner.state",
        copy=False,
        tracking=True,
    )
    customer_business_area_ids = fields.Many2many(
        string="Business areas", comodel_name="res.partner.business.area", copy=False
    )
