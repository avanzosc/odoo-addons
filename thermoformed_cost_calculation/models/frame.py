# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class Frame(models.Model):
    _name = 'frame'
    _description = 'Frame'

    name = fields.Char(string='Name')
    workcenter_id = fields.Many2one(
        string='Workcenter',
        comodel_name='mrp.workcenter')
    width = fields.Float(
        string='Width')
    step = fields.Float(
        string='Step')
    description = fields.Char(
        string='Description')
