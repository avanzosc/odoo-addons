# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResAreaType(models.Model):
    _name = 'res.area.type'
    _description = 'Area types'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    area_ids = fields.Many2many(
        string="Areas", comodel_name="res.area",
        relation="rel_area_area_type", columm1="res_area_type_id",
        columm2='res_area_id', copy=False)
