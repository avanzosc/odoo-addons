# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_type_id = fields.Many2one(comodel_name='sale.order.type',
                                   string="Partial orders type")
    # sale_manager_users = fields.Many2many(
    #     comodel_name="res.users", computed="_computed_sale_manager_users")
    sale_manager_validations = fields.One2many(
        comodel_name="sale.manager.lines", inverse_name="settings_id")

    # @api.depends('sale_manager_users')
    # def _computed_manager_lines(self):
    #     validation_users = self.sale_manager_validations.mapped('user_id')
    #     remove_users = validation_users - self.sale_manager_users
    #     add_users = self.sale_manager_users - validation_users
    #     for line in self.sale_manager_validations.filtered(lambda x:
    #             x.user_id in remove_users):
    #         self.sale_manager_validations = [(2, line.id)]
    #     new_users = []
    #     for user in add_users:
    #         new_users.append((0, 0, {'user_id': user.id}))
    #     self.sale_manager_validations = new_users
    #
    # @api.multi
    # def _computed_sale_manager_users(self):
    #     sale_manager_group = self.env.ref("base.group_sale_manager")
    #     self.sale_manager_users = [(6, 0, sale_manager_group.users.ids)]

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
            'sale_manager_validations': get_value(
                'sale.manager.validations', False),
        }

    @api.multi
    def set_parameters(self):
        self._write_or_create_param('sale.manager.validations',
                                    self.sale_manager_validations.ids)


class SaleManagerLines(models.Model):
    _name = "sale.manager.lines"

    user_id = fields.Many2one(comodel_name="res.users")
    notification = fields.Boolean(string="Notification", default=True)
    validation = fields.Boolean(string="Validation", default=False)
    settings_id = fields.Many2one(comodel_name='res.company')
