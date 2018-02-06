# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class OrderCondition(models.AbstractModel):
    _name = 'order.condition'
    _description = 'Order Condition Abstract'

    condition_id = fields.Many2one(
        comodel_name='contract.condition', string='Condition')
    sequence = fields.Integer(string='Sequence')
    description = fields.Text(string='Description', required=True)
    comments = fields.Text(string='Comments')
    section_id = fields.Many2one(
        comodel_name='contract.section', string='Section')
    type_id = fields.Many2one(
        comodel_name='contract.condition.type', string='Type')
    selected = fields.Boolean(string='Selected')

    @api.onchange('condition_id')
    def _onchange_condition_id(self):
        if self.condition_id:
            self.sequence = self.condition_id.sequence
            self.description = (
                self.condition_id.description or self.condition_id.name)
            self.comments = self.condition_id.comments or ''
            self.section_id = self.condition_id.section_id
            self.type_id = self.condition_id.type_id
            self.selected = self.condition_id.selected
