# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_medical_record_ids = fields.One2many(
        string='Partner Medical Record Number',
        comodel_name='medical.record.number',
        inverse_name='partner_id')
    parent_medical_record_ids = fields.One2many(
        string='Parent Medical Record Number',
        comodel_name='medical.record.number',
        inverse_name='parent_id',
        related='parent_id.partner_medical_record_ids')

    def action_view_medical_record(self):
        context = self.env.context.copy()
        context.update({'default_partner_id': self.id})
        medical_record = self.env['medical.record.number']
        if self.parent_id:
            context.update({'default_parent_id': self.parent_id.id})
        if self.partner_medical_record_ids:
            medical_record += max(
                self.partner_medical_record_ids, key=lambda x: x.number)
        if self.parent_medical_record_ids:
            medical_record += max(
                self.parent_medical_record_ids, key=lambda x: x.number)
        if medical_record:
            return {
                'name': _("Medical record number"),
                'view_mode': 'tree',
                'res_model': 'medical.record.number',
                'domain': [('id', 'in', medical_record.ids)],
                'type': 'ir.actions.act_window',
                'context': context
            }
