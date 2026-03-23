# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerMarket(models.Model):
    _name = "res.partner.market"
    _description = "Market"

    name = fields.Char(string="Description")
