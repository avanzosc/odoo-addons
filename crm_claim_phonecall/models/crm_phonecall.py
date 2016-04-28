# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    @api.onchange('claim_id')
    def onchange_claim_id(self):
        self.partner_id = self.claim_id.partner_id

    @api.multi
    def make_call(self):
        self.state = 'pending'

    @api.multi
    def hang_up_call(self):
        self.state = 'done'

    @api.multi
    def cancel_call(self):
        self.state = 'cancel'

    @api.multi
    def write(self, values):
        if values.get('state'):
            if values.get('state') == 'pending':
                values['date_open'] = fields.datetime.now()
                values['duration'] = 0.0
        return super(CrmPhonecall, self).write(values)

    @api.multi
    def compute_duration(self):
        for phonecall in self:
            if phonecall.duration <= 0:
                duration = datetime.now() - \
                    datetime.strptime(phonecall.date_open,
                                      DEFAULT_SERVER_DATETIME_FORMAT)
                values = {'duration': duration.seconds/float(60)}
                self.write(values)
        return True

    claim_id = fields.Many2one(comodel_name='crm.claim',
                               string='Claim')
