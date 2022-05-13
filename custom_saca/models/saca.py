# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta
from odoo import fields, models, _


class Saca(models.Model):
    _name = "saca"
    _description = "Saca"

    def _default_date(self):
        today = fields.Date.today()
        return today + relativedelta(days=1)

    name = fields.Char(
        string='Name', required=True, copy=False, index=True,
        default=lambda self: _('New'))
    date = fields.Date(string='Date', default=_default_date)
    saca_line_ids = fields.One2many(
        string='Saca Line', comodel_name='saca.line', inverse_name='saca_id')
    line_count = fields.Integer(
        '# Saca Lines', compute='_compute_saca_line_count')

    def _compute_saca_line_count(self):
        for saca in self:
            saca.line_count = len(saca.saca_line_ids)

    def action_view_saca_line(self):
        context = self.env.context.copy()
        context.update({'default_saca_id': self.id})
        return {
            'name': _("Saca Lines"),
            'view_mode': 'tree,form',
            'res_model': 'saca.line',
            'domain': [('id', 'in', self.saca_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }