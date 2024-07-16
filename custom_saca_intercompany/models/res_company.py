# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    paasa = fields.Boolean(string="PAASA", default=False)
    tolvasa = fields.Boolean(string="Tolvasa", default=False)
