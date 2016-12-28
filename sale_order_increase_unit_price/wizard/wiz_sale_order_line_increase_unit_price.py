# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class WizSaleOrderLineIncreaseUnitPrice(models.TransientModel):
    _name = 'wiz.sale.order.line.increase.unit.price'
    _description = 'Wizard for increase sale order line unit price'

    increase = fields.Float(
        string='Increase', digits=(1, 3), required=True, default=0.014,
        help='By default an increase in the unit price of 1.4%')
    contract = fields.Boolean(
        string='Increase price unit in sale contract lines')
    materials_services = fields.Boolean(
        string='With materials or services')
    materials = fields.Boolean(
        string='Only with materials')
    services = fields.Boolean(
        string='Only with services')

    @api.onchange('materials_services')
    def onchange_materials_services(self):
        if self.materials_services:
            self.materials = False
            self.services = False

    @api.onchange('materials')
    def onchange_materials(self):
        if self.materials:
            self.materials_services = False
            self.services = False

    @api.onchange('services')
    def onchange_services(self):
        if self.services:
            self.materials_services = False
            self.materials = False

    @api.multi
    def apply_increase(self):
        if not self.increase:
            raise exceptions.Warning(
                _('You must indicate the increment'))
        if (not self.contract and not self.materials_services and not
                self.materials and not self.services):
            raise exceptions.Warning(
                _('You must indicate where to apply the increment'))
        sales = self.env['sale.order'].browse(
            self.env.context.get('active_ids')).filtered(
            lambda x: x.state in ('draft', 'send'))
        if self.contract:
            for sale in sales.filtered(
                    lambda x: x.project_id and
                    x.project_id.recurring_invoice_line_ids):
                for line in sale.project_id.mapped(
                        'recurring_invoice_line_ids').filtered(
                        lambda x: x.price_unit):
                    line.price_unit = (
                        line.price_unit + (line.price_unit * self.increase))
        lines = []
        if self.materials_services:
            lines = sales.mapped('order_line')
        elif self.materials:
            lines = sales.mapped('order_line').filtered(
                lambda x: x.product_id.type != 'service')
        elif self.services:
            lines = sales.mapped('order_line').filtered(
                lambda x: x.product_id.type == 'service')
        for line in lines:
            line.price_unit = (
                line.price_unit + (line.price_unit * self.increase))
