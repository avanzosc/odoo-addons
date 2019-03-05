# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(
        selection_add=[('for management approval', 'For Management Approval')])

    @api.multi
    def button_approve(self, force=False):
        currency = self.env.user.company_id.currency_id
        for order in self:
            if order.state not in ['draft', 'sent', 'to approve',
                                   'for management approval']:
                continue
            if (order.state not in ['to approve'] or
                    order.amount_total < currency.compute(
                order.company_id.po_double_validation_amount2,
                order.currency_id) or
                order.user_has_groups(
                    'purchase_amount_validation.group_purchase_head')):
                super(PurchaseOrder, order).button_approve(force=force)
            else:
                order.write({'state': 'for management approval'})
        return {}
