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
        month = datetime.strptime(fec_ini, '%Y-%m-%d').date().month
        if ((line.january and month == 1) or
            (line.february and month == 2) or
            (line.march and month == 3) or
            (line.april and month == 4) or
            (line.may and month == 5) or
            (line.june and month == 6) or
            (line.july and month == 7) or
            (line.august and month == 8) or
            (line.september and month == 9) or
            (line.october and month == 10) or
            (line.november and month == 11) or
                (line.december and month == 12)):
            valid = True
        return valid

    def _validate_event_session_week(self, line, num_week):
        valid = False
        if ((line.week1 and num_week == 1) or
            (line.week2 and num_week == 2) or
            (line.week3 and num_week == 3) or
            (line.week4 and num_week == 4) or
                (line.week5 and num_week == 5)):
            valid = True
        return valid

    def _validate_event_session_day(self, line, fec_ini):
        valid = False
        day = datetime.strptime(fec_ini, '%Y-%m-%d').date().weekday()
        if ((line.monday and day == 0) or
            (line.tuesday and day == 1) or
            (line.wednesday and day == 2) or
            (line.thursday and day == 3) or
            (line.friday and day == 4) or
            (line.saturday and day == 5) or
                (line.sunday and day == 6)):
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
