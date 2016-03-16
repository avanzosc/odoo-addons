# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmPhonecall2phonecall(models.TransientModel):
    _inherit = 'crm.phonecall2phonecall'

    claim_id = fields.Many2one(comodel_name='crm.claim', string='Claim')

    @api.multi
    def action_schedule(self):
        res = super(CrmPhonecall2phonecall, self).action_schedule()
        phonecall = self.env['crm.phonecall'].browse(res['res_id'])
        for this in self:
            if this.claim_id:
                phonecall.write({'claim_id': this.claim_id.id})
        return phonecall.redirect_phonecall_view(phonecall)

    @api.model
    def default_get(self, fields):
        res = super(CrmPhonecall2phonecall, self).default_get(fields)
        context = self.env.context
        active_id = context and context.get('active_id', False) or False
        if active_id:
            phonecall = self.env['crm.phonecall'].browse(active_id)
            if phonecall.claim_id:
                res.update({'claim_id': phonecall.claim_id and
                            phonecall.claim_id.id or False})
        return res
