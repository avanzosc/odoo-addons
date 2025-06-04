# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    rsipac_code = fields.Char(
        string="RSIPAC",
        related="partner_id.rsipac_code",
        readonly=False,
    )
