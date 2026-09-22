# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerInteres(models.Model):
    _name = "res.partner.interes"
    _description = "interest"

    name = fields.Char("Description", required=True, index=True)
    partner_id = fields.One2many(
        string="Customer", comodel_name="res.partner", inverse_name="interest_id"
    )
