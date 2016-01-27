# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        self._create_event_and_sessions_from_sale_order()
        return res

    def _create_event_and_sessions_from_sale_order(self):
        event_obj = self.env['event.event']
        project_obj = self.env['project.project']
        for sale in self:
            cond = [('analytic_account_id', '=', sale.project_id.id)]
            project = project_obj.search(cond, limit=1)
            event_vals = ({'name': sale.name,
                           'date_begin': sale.project_id.date_start,
                           'date_end': sale.project_id.date,
                           'project_id': project.id})
            event = event_obj.create(event_vals)
            sale.project_id.date = event_vals.get('date_end')
            sale_lines = sale.order_line.filtered(
                lambda x: x.recurring_service)
            for line in sale_lines:
                num_session = 0
                sale._validate_create_session_from_sale_order(
                    event, num_session, line)

    def _validate_create_session_from_sale_order(
            self, event, num_session, line):
        fec_ini = self.project_id.date_start
        if datetime.strptime(fec_ini, '%Y-%m-%d').date().day != 1:
            while datetime.strptime(fec_ini, '%Y-%m-%d').date().day != 1:
                fec_ini = fields.Date.to_string(
                    fields.Date.from_string(fec_ini) + relativedelta(days=-1))
        if datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 0:
            num_week = 0
        else:
            num_week = 1
        month = datetime.strptime(fec_ini, '%Y-%m-%d').date().month
        while fec_ini <= self.project_id.date:
            if month != datetime.strptime(fec_ini, '%Y-%m-%d').date().month:
                month = datetime.strptime(fec_ini, '%Y-%m-%d').date().month
                if (datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() ==
                        0):
                    num_week = 0
                else:
                    num_week = 1
            if (datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 0):
                num_week += 1
            if fec_ini >= self.project_id.date_start:
                valid = self._validate_event_session_month(line, fec_ini)
                if valid:
                    valid = self._validate_event_session_week(
                        line, num_week)
                if valid:
                    valid = self._validate_event_session_day(line, fec_ini)
                if valid:
                    num_session += 1
                    self._create_session_from_sale_line(
                        event, num_session, line, fec_ini)
            fec_ini = fields.Date.to_string(
                fields.Date.from_string(fec_ini) + relativedelta(days=+1))

    def _validate_event_session_month(self, line, fec_ini):
        valid = False
        if (line.january and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 1):
            valid = True
        if (line.february and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 2):
            valid = True
        if (line.march and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 3):
            valid = True
        if (line.april and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 4):
            valid = True
        if (line.may and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 5):
            valid = True
        if (line.june and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 6):
            valid = True
        if (line.july and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 7):
            valid = True
        if (line.august and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 8):
            valid = True
        if (line.september and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 9):
            valid = True
        if (line.october and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 10):
            valid = True
        if (line.november and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 11):
            valid = True
        if (line.december and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().month == 12):
            valid = True
        return valid

    def _validate_event_session_week(self, line, num_week):
        valid = False
        if line.week1 and num_week == 1:
            valid = True
        if line.week2 and num_week == 2:
            valid = True
        if line.week3 and num_week == 3:
            valid = True
        if line.week4 and num_week == 4:
            valid = True
        if line.week5 and num_week == 5:
            valid = True
        return valid

    def _validate_event_session_day(self, line, fec_ini):
        valid = False
        if (line.monday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 0):
            valid = True
        if (line.tuesday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 1):
            valid = True
        if (line.wednesday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 2):
            valid = True
        if (line.thursday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 3):
            valid = True
        if (line.friday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 4):
            valid = True
        if (line.saturday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 5):
            valid = True
        if (line.sunday and
                datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday() == 6):
            valid = True
        return valid

    def _create_session_from_sale_line(
            self, event, num_session, line, date):
        if line.performance:
            duration = (line.performance * line.product_uom_qty)
        else:
            duration = line.product_uom_qty
        vals = {'name': (_('Session %s for %s') % (str(num_session),
                                                   line.product_id.name)),
                'event_id': event.id,
                'date': date,
                'duration': duration}
        session = self.env['event.track'].create(vals)
        session.tasks = [(4, line.service_project_task.id)]
        duration = sum(line.service_project_task.sessions.mapped('duration'))
        line.service_project_task.planned_hours = duration
