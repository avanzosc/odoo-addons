# -*- coding: utf-8 -*-
# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'
    number_price_field = fields.Selection(
        selection=[('2', '2'), ('3', '3'), ('4', '4')],
        string='Prices in products')

    def _get_parameter(self, key, default=False):
        param_obj = self.env['ir.config_parameter']
        rec = param_obj.search([('key', '=', key)])
        return rec or default

    @api.multi
    def get_default_number_price_field(self):
        def get_value(key, default=''):
            rec = self._get_parameter(key)
            return rec and rec.value or default
        return {
            'number_price_field': get_value('number.price.field', False),
        }

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
    def set_number_price_field(self):
        self._write_or_create_param('number.price.field',
                                    self.number_price_field)
