# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    contract_line_id = fields.Many2one(
        string='Contract line', comodel_name='contract.line')
    contract_id = fields.Many2one(
        string='Contract', comodel_name='contract.contract',
        related='contract_line_id.contract_id', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if ('contract_line_id' not in vals and
                'sale_order_line_id' in vals and
                    vals.get('sale_order_line_id', False)):
                line = self.env['sale.order.line'].browse(
                    vals.get('sale_order_line_id'))
                if line.contract_line_id:
                    vals['contract_line_id'] = line.contract_line_id.id
        return super(EventRegistration, self).create(vals_list)

    def write(self, vals):
        if ('contract_line_id' not in vals and
            'sale_order_line_id' in vals and
                vals.get('sale_order_line_id', False)):
            line = self.env['sale.order.line'].browse(
                vals.get('sale_order_line_id'))
            if line.contract_line_id:
                vals['contract_line_id'] = line.contract_line_id.id
        return super(EventRegistration, self).write(vals)
