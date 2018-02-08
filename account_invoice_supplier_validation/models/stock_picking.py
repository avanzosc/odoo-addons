# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        partner, currency_id, company_id, user_id = key
        if inv_type in ('in_invoice', 'in_refund'):
            department = partner.hr_department
            if department and department.manager_id.user_id:
                key = (partner, currency_id, company_id,
                       department.manager_id.user_id.id)
        return super(StockPicking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
