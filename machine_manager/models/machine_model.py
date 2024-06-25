# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class MachineModel(models.Model):
    _name = "machine.model"
    _description = "Machine model"

    name = fields.Char(string="Name")
    model_type = fields.Char(string="Type")
