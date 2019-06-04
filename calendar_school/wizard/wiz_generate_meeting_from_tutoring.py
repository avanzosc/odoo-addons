# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizGenerateMeetingFromTutoring(models.TransientModel):
    _name = "wiz.generate.meeting.from.tutoring"
    _description = "Generate meetings from tutoring"

    @api.multi
    def meetings_confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        meetings = self.env['hr.employee.supervised.year'].browse(active_ids)
        if meetings:
            meetings.generate_meetings()
        return {'type': 'ir.actions.act_window_close'}
