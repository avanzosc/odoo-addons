# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta


class Saca(models.Model):
    _name = "saca"
    _description = "Saca"

    def _default_date(self):
        today = fields.Date.today()
        return today

    def _default_name(self):
        today = fields.Date.today()
        today = today + relativedelta(days=1)
        today = u'{}'.format(today)
        today = today.replace("-", "")
        today = today[2:]
        return today

    name = fields.Char(
        string='Name', required=True, copy=False, default=_default_name)
    date = fields.Date(string='Date', default=_default_date)
    saca_line_ids = fields.One2many(
        string='Saca Line', comodel_name='saca.line', inverse_name='saca_id')
    line_count = fields.Integer(
        '# Saca Lines', compute='_compute_saca_line_count')
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        default=lambda self: self.env.company.id,
        required=True)

    def _compute_saca_line_count(self):
        for saca in self:
            saca.line_count = len(saca.saca_line_ids)

    @api.onchange("date")
    def onchange_date(self):
        if self.date:
            name = u'{}'.format(self.date + relativedelta(days=1))
            name = name.replace("-", "")
            name = name[2:]
            self.name = name

    def action_view_saca_line(self):
        context = self.env.context.copy()
        context.update({
            'default_saca_id': self.id,
            'default_lot': self.name})
        return {
            'name': _("Saca Lines"),
            'view_mode': 'tree,form',
            'res_model': 'saca.line',
            'domain': [('id', 'in', self.saca_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
