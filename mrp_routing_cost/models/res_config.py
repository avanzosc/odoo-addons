# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpConfigSettings(models.TransientModel):
    _inherit = 'mrp.config.settings'

    subtotal_by_unit = fields.Boolean(
        string='Compute unitary total values',
        help='This will allow you to define if the total of the scheduled '
        'product list is computed by unit or not.')

    def _get_parameter(self, key, default=False):
        param_obj = self.env['ir.config_parameter']
        rec = param_obj.search([('key', '=', key)])
        return rec or default

    def _write_or_create_param(self, key, value):
        param_obj = self.env['ir.config_parameter']
        rec = self._get_parameter(key)
        if rec:
            if not value:
                rec.unlink()
            else:
                rec.value = value
        elif value:
            param_obj.create({'key': key, 'value': value})

    @api.multi
    def get_default_parameters(self):
        def get_value(key, default=''):
            rec = self._get_parameter(key)
            return rec and rec.value or default
        return {
            'subtotal_by_unit': get_value('subtotal.by.unit', False),
        }

    @api.multi
    def set_parameters(self):
        self._write_or_create_param('subtotal.by.unit', self.subtotal_by_unit)
