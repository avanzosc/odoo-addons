# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    extra_phone_ids = fields.One2many(
        string="Extra Phones", comodel_name="extra.phone", inverse_name="partner_id"
    )
