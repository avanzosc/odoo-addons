# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResTarget(models.Model):
    _name = 'res.target'
    _description = 'Targets'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
