# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def claim_re_open(self):
        self.date_closed = False
        self.stage_id = self._get_default_stage_id()

    @api.multi
    def claim_close(self):
        self.date_closed = fields.Datetime.now()
