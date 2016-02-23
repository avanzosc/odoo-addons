# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventTrack(models.Model):
    _inherit = 'event.track'

    tasks = fields.Many2many(
        comodel_name="project.task", relation="task_session_project_relation",
        column1="track_id", column2="task_id", copy=False, string="Tasks")


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.multi
    def registration_open(self):
        self.ensure_one()
        event_obj = self.env['event.event']
        wiz_obj = self.env['wiz.event.append.assistant']
        result = super(EventRegistration, self).registration_open()
        event = event_obj.browse(result['context']['event_id'])
        wiz = wiz_obj.browse(result['res_id'])
        wiz.update({'tasks': [(6, 0, event.task_ids.ids)]})
        return result
