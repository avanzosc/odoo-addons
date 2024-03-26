# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class VisitType(models.Model):
    _name = "visit.type"
    _description = "Visit Type"
    _order = "name"

    name = fields.Char(string="Description", required=True, copy=False)
