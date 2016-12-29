# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class WizSaleOrderLineIncreaseUnitPrice(models.TransientModel):
    _inherit = 'wiz.sale.order.line.increase.unit.price'

    contract = fields.Boolean(
        string='Increase price unit in sale contract lines')

    @api.multi
    def apply_increase(self):
        super(WizSaleOrderLineIncreaseUnitPrice, self).apply_increase()
        if self.contract:
            sales = self.env['sale.order'].browse(
                self.env.context.get('active_ids')).filtered(
                lambda x: x.state in ('draft', 'send') and x.project_id and
                x.project_id.recurring_invoice_line_ids)
            for line in sales.mapped(
                    'project_id.recurring_invoice_line_ids').filtered(
                    lambda x: x.price_unit):
                line.price_unit = line.price_unit + (line.price_unit *
                                                     self.increase)

    def _validate_wizard_fields(self):
        if not self.increase:
            raise exceptions.Warning(
                _('You must indicate the increment'))
        if (not self.contract and not self.materials_services and not
                self.materials and not self.services):
            raise exceptions.Warning(
                _('You must indicate where to apply the increment'))
