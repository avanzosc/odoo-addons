# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class OrderCondition(models.AbstractModel):
    _name = 'order.condition'
    _description = 'Order Condition Abstract'

    condition_id = fields.Many2one(
        comodel_name='contract.condition', string='Condition')
    description = fields.Text(string='Description', required=True)

    @api.onchange('condition_id')
    def _onchange_condition_id(self):
        if self.condition_id:
            self.description = (
                self.condition_id.description or self.condition_id.name)
