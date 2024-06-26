# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerMarket(models.Model):
    _name = "res.partner.market"
    _description = "Customer market"
    _order = "name"

    name = fields.Char(string="Description", required=True, copy=False)
