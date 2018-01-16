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
    materials_services = fields.Boolean(
        string='In lines with materials or services')
    materials = fields.Boolean(
        string='In lines only with No services')
    services = fields.Boolean(
        string='In lines only with services')

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
        self._validate_wizard_fields()
        sales = self.env['sale.order'].browse(
            self.env.context.get('active_ids')).filtered(
            lambda x: x.state != 'cancel')
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

    def _validate_wizard_fields(self):
        if not self.increase:
            raise exceptions.Warning(
                _('You must indicate the increment'))
        if (not self.materials_services and not self.materials and not
                self.services):
            raise exceptions.Warning(
                _('You must indicate where to apply the increment'))
