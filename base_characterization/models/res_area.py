# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResArea(models.Model):
    _name = 'res.area'
    _description = 'Areas'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type_ids = fields.Many2many(
        string="Area Types", comodel_name="res.area.type",
        relation="rel_area_area_type", columm1="res_area_id",
        columm2='res_area_type_id', copy=False)
