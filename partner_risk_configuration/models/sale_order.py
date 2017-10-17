# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        if not self.env.context.get('bypass_risk', False):
            for order in self:
                partner = order.partner_id.get_risk_partner()
                exception_msg = ""
                if partner.risk_exception:
                    exception_msg = _("Financial risk exceeded.\n")
                elif partner.risk_sale_order_limit and (
                        (partner.risk_sale_order + self.amount_total) >
                        partner.risk_sale_order_limit):
                    exception_msg = _(
                        "This sale order exceeds the sales orders risk.\n")
                elif partner.risk_sale_order_include and (
                        (partner.risk_total + self.amount_total) >
                        partner.credit_limit):
                    exception_msg = _(
                        "This sale order exceeds the financial risk.\n")
                if exception_msg:
                    return self.env['partner.risk.exceeded.wiz'].create({
                        'exception_msg': exception_msg,
                        'partner_id': partner.id,
                        'origin_reference': '%s,%s' % (self._model, self.id),
                        'continue_method': 'action_button_confirm',
                    }).action_show()
        return super(SaleOrder, self.with_context(bypass_risk=True)
                     ).action_button_confirm()
