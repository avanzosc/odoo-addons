
from odoo import fields, models
from odoo.exceptions import ValidationError


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    responsible_user_ids = fields.Many2one(
        'res.users', 'Input responsibles',
        compute='_compute_responsible_users')


    def _compute_responsible_users(self):
        for res in self:
            res.responsible_user_ids = res.user_input_ids.mapped(
                'main_responsible_id')

    def get_filtered_surveys(self):
        if self._context.get('params', False):
            params = self._context.get('params', False)
            if params.get('menu_id', False):
                raise ValidationError(
                    "Attention:You are not allowed to access this page due to Security Policy. In case of any query, please contact ERP Admin or Configuration Manager.")
        else:
            return False
        view_id_form = self.env['ir.ui.view'].search(
            [('xml_id', '=', 'survey.survey_form')])
        view_id_tree = self.env['ir.ui.view'].search(
            [('xml_id', '=', 'survey.survey_tree')])
        view_id_kanban = self.env['ir.ui.view'].search(
            [('xml_id', '=', 'survey.survey_kanban')])
        user = self.env['res.users'].browse(self._uid)
        return {
            'type': 'ir.actions.act_window',
            # 'name': _('My Surveys'),
            'res_model': 'survey.survey',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            # 'view_id': view_id_tree.id,
            'views': [
                (view_id_kanban.id, 'kanban'),
                (view_id_tree.id, 'tree'),
                (view_id_form.id, 'form')],
            'target': 'current',
            'domain': [('responsible_user_ids', 'in', [user.id])]
            # 'res_id': your.model.id,
        }


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    student_id = fields.Many2one('res.partner', 'Student')
    event_id = fields.Many2one('event.event', 'Event')
    main_responsible_id = fields.Many2one(
        'res.users', 'Main responsible',
        related='event_id.main_responsible_id')
    second_responsible_id = fields.Many2one(
        'res.users', 'Second responsible',
        related='event_id.second_responsible_id')
