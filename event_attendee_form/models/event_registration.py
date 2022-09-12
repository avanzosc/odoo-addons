# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    remarks = fields.Char('General remarks')
    diversity_attention = fields.Char('Attention to diversity')
    allergies = fields.Char('Food allergies or intolerances')

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration,
                    self)._get_website_registration_allowed_fields()
        res.update({'remarks', 'diversity_attention', 'allergies'})
        return res

    @api.depends('remarks', 'diversity_attention', 'allergies')
    def onchange_custom_fields(self):
        self.ensure_one()
        concat_sentence = ''
        if self.remarks:
            concat_sentence += _('General remarks: ') + self.remarks + '\n'
        if self.diversity_attention:
            concat_sentence += _('Attention to diversity: ') \
                               + self.diversity_attention + '\n'
        if self.allergies:
            concat_sentence += _('Food allergies or intolerances: ') \
                               + self.allergies + '\n'
        if len(concat_sentence) > 1 and self.student_id and self.student_id.comment:
            self.student_id.comment += '\n\n' + concat_sentence

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        for record in self:
            record.onchange_custom_fields()
        return result
