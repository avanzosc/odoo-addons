# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    paasa = fields.Boolean(default=False)
    tolvasa = fields.Boolean(default=False)
    proalpe = fields.Boolean(default=False)
