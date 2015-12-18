# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
from dateutil.relativedelta import relativedelta


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def _get_date_deadline(self):
        if self.env.user.company_id.claim_closing_days:
            return fields.Date.to_string(
                fields.Date.from_string(fields.Date.context_today(self)) +
                relativedelta(
                    days=self.env.user.company_id.claim_closing_days))
        return False

    date_deadline = fields.Date(default=_get_date_deadline)

    @api.onchange('company_id')
    def onchange_company_id(self):
        self.date_deadline = False
        if self.company_id.claim_closing_days:
            self.date_deadline = fields.Date.to_string(
                fields.Date.from_string(fields.Date.context_today(self)) +
                relativedelta(days=self.company_id.claim_closing_days))
