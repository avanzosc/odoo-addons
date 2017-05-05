# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    claim_id = fields.Many2one(comodel_name='crm.claim', string='Claim')

    def on_change_account_id(self, cr, uid, ids, account_id, context=False):
        """Signature cannot be new API because of the arguments are badly
        named between hr_timesheet and hr_timesheet_invoice.
        """
        res = super(HrAnalyticTimesheet, self).on_change_account_id(
            cr, uid, ids, account_id, context)
        if account_id:
            if 'domain' not in res:
                res['domain'] = {}
            res['domain']['claim_id'] = [('analytic_id', '=', account_id)]
        return res
