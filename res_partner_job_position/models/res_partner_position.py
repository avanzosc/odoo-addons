# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerFunction(models.Model):
    _name = "res.partner.function"
    _description = "Job positions"

    name = fields.Char(string="Description", required=True)
