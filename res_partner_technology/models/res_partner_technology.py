# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerTechnology(models.Model):
    _name = "res.partner.technology"
    _description = "Customer technology"
    _order = "name"

    name = fields.Char(string="Description", required=True, copy=False)
