# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrModelUrl(models.Model):
    _name = 'ir.model.url'

    name = fields.Char(string="Name", related="ir_model_id.name")
    ir_model_id = fields.Many2one(comodel_name='ir.model', string="Model")
    url = fields.Char(string="Portal URL")
