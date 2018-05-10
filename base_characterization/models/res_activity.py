# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResActivity(models.Model):
    _name = 'res.activity'
    _description = 'Activities'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
