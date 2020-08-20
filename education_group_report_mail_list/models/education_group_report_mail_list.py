# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class EducationGroupStudentReport(models.Model):
    _inherit = 'education.group.student.report'

    @api.multi
    def include_on_lists(self):
        context = self.env.context.copy()
        context['active_id'] = self.id
        context['active_ids'] = [self.id]
        context['active_model'] = 'education.group.student.report'
        return {
            'name': ('Include on mailing list'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'education.group.student.report.wizard',
            'target': 'new',
            'context': context,
            }
