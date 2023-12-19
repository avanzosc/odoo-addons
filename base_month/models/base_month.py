# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class BaseMonth(models.Model):
    _name = 'base.month'
    _description = 'Months of the year'

    name = fields.Char(string='Month', translate=True, required=True)
    number = fields.Integer(string='Number of month', required=True)
