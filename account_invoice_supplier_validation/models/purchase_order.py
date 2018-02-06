# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def _prepare_invoice(self, order, line_ids):
        res = super(PurchaseOrder, self)._prepare_invoice(order, line_ids)
        department = order.partner_id.hr_department
        if department and department.manager_id.user_id:
            res.update({'user_id': department.manager_id.user_id.id})
        return res
