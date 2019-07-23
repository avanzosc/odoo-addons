# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning
from odoo.addons.calendar.models.calendar import calendar_id2real_id


class CalendarUserInput(models.TransientModel):
    _name = 'calendar.user_input'
    _description = 'Create Survey User Input For Events'

    event_id = fields.Many2one(comodel_name='calendar.event', required=True)
    survey_ids = fields.Many2many(comodel_name='survey.survey')
    partner_ids = fields.Many2many(
        comodel_name='res.partner', string='Attendees')

    @api.model
    def default_get(self, fields):
        res = super(CalendarUserInput, self).default_get(fields)
        context = self.env.context
        assert context.get('active_model') == 'calendar.event',\
            'active_model should be calendar.event'
        assert context.get('active_id'), 'Missing active_id in context !'
        event_id = calendar_id2real_id(context.get('active_id'))
        event = self.env['calendar.event'].browse(event_id)
        res.update({
            'event_id': event.id,
            'survey_ids': event.mapped('categ_ids.survey_ids').ids,
            'partner_ids': event.mapped('partner_ids').ids,
        })
        return res

    @api.multi
    def create_survey_response(self):
        if not self.survey_ids or not self.partner_ids:
            raise Warning(
                _('You must select at least a survey and a attendee.'))
        response_obj = self.env['survey.user_input']
        real_id = calendar_id2real_id(self.event_id.id)
        for survey in self.survey_ids:
            for partner in self.partner_ids:
                response = response_obj.search([
                    ('event_id', '=', real_id),
                    ('survey_id', '=', survey.id),
                    ('partner_id', '=', partner.id),
                ])
                # create a response and link it to this applicant
                if not response:
                    response_obj.create({
                        'event_id': real_id,
                        'survey_id': survey.id,
                        'partner_id': partner.id,
                        'type': 'manually',
                    })
        return True
