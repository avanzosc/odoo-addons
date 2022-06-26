# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizEventAttendanceReport(models.TransientModel):
    _inherit = 'wiz.event.attendance.report'

    allowed_lang_ids = fields.Many2many(
        string="Allowed langs", comodel_name="hr.skill",
        relation='rel_wiz_event_attendance_report_lang',
        column1='wiz_id', column2='allowed_lang_id')
    allowed_level_ids = fields.Many2many(
        string="Allowed levels", comodel_name="hr.skill.level",
        relation='rel_wiz_event_attendance_report_level',
        column1='wiz_id', column2='allowed_level_id')
    lang_id = fields.Many2one(
        string='Language', comodel_name='hr.skill')
    level_id = fields.Many2one(
        string='Level', comodel_name='hr.skill.level')

    @api.onchange("lang_id")
    def _onchange_lang_id(self):
        self.put_allowed_data()

    @api.onchange("level_id")
    def _onchange_level_id(self):
        self.put_allowed_data()

    def set_allowed_data(self):
        lines = super(
            WizEventAttendanceReport, self).set_allowed_data()
        langs = lines.mapped('lang_id')
        levels = lines.mapped('level_id')
        self.allowed_lang_ids = [(6, 0, langs.ids)]
        self.allowed_level_ids = [(6, 0, levels.ids)]
        return lines

    def filter_lines(self, lines):
        lines = super(WizEventAttendanceReport, self).filter_lines(lines)
        if self.level_id:
            lines = lines.filtered(
                lambda x: x.level_id.id == self.level_id.id)
        if self.lang_id:
            lines = lines.filtered(
                lambda x: x.lang_id.id == self.lang_id.id)
        return lines

    def count_num_filters(self, cont):
        cont = super(WizEventAttendanceReport, self).count_num_filters(cont)
        if self.level_id:
            cont += 1
        if self.lang_id:
            cont += 1
        return cont
