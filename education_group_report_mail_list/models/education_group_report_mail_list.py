
from odoo import api, fields, models


class EducationGroupStudentProgenitorReport(models.Model):
    _inherit = 'education.group.student.progenitor.report'
    
    @api.multi
    def include_on_lists(self):
        context = self.env.context.copy()
        context['active_id'] = self.id
        context['active_ids'] = [self.id]
        context['active_model'] = 'education.group.student.progenitor.report'
        return {
            'name': ('Include on mailing list'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'update.progenitor.into.mail.list.wizard',
            'target': 'new',
            'context': context,
            }

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
            'res_model': 'update.student.into.mail.list.wizard',
            'target': 'new',
            'context': context,
            }
