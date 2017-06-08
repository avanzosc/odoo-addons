# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class WizCalculateWorkableFestive(models.TransientModel):
    _name = 'wiz.calculate.workable.festive'
    _description = 'Wizard for calculate workables and festives'

    year = fields.Integer(
        string='Employee calendar year', size=4, required=True)

    @api.model
    def default_get(self, var_fields):
        partner_calendar_obj = self.env['res.partner.calendar']
        res = super(WizCalculateWorkableFestive, self).default_get(var_fields)
        contract = self.env['hr.contract'].browse(
            self.env.context['active_id'])
        year_begin = fields.Datetime.from_string(contract.date_start).year
        cond = [('partner', '=', contract.partner.id),
                ('year', '=', year_begin)]
        calendar = partner_calendar_obj.search(cond, limit=1)
        if not calendar:
            res.update({'year': year_begin})
        else:
            if contract.date_end:
                year_end = fields.Datetime.from_string(contract.date_end).year
                if year_begin == year_end:
                    res.update({'year': year_begin})
        return res

    @api.multi
    def button_calculate_workables_and_festives(self):
        self.ensure_one()
        contract = self.env['hr.contract'].browse(
            self.env.context['active_id'])
        date_begin = fields.Date.from_string(contract.date_start)
        if self.year < date_begin.year:
            raise exceptions.Warning(
                _('Year introduced less than year contract beginning'))
        if contract.date_end:
            date_end = fields.Datetime.from_string(contract.date_end)
            if self.year > date_end.year:
                raise exceptions.Warning(
                    _('Year introduced more than year end contract'))
        contract._generate_calendar_from_wizard(self.year)
