# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields
from odoo import tools


class EventAttendanceReport(models.Model):
    _name = "event.attendance.report"
    _description = "Event attendance report"
    _auto = False
    _rec_name = 'event_name'
    _order = 'customer_name, event_name, session_date, student_name'

    company_id = fields.Many2one(
        string='Company', comodel_name='res.company', readonly="1")
    event_id = fields.Many2one(
        string="Event", comodel_name="event.event", readonly="1")
    event_name = fields.Char(
        string="Event name", readonly="1")
    session_date = fields.Date(
        string="Session Date", readonly="1")
    planned_hours = fields.Float(
        string="Planned hours", readonly="1")
    real_hours = fields.Float(
        string="Real hours", readonly="1")
    customer_id = fields.Many2one(
        string="Customer", comodel_name='res.partner', readonly="1")
    customer_name = fields.Char(
        string="Customer name", readonly="1")
    student_id = fields.Many2one(
        string="Student", comodel_name='res.partner', readonly="1")
    student_name = fields.Char(
        string="Student name", readonly="1")

    def _select_event_attendace_report(self):
        select_ = """
            CAST(rpad(CAST(t.id AS TEXT), 8, '0') as Integer) +
            r.partner_id + r.student_id as id,
            e.company_id as company_id,
            t.event_id as event_id,
            e.name as event_name,
            to_date(to_char(t.date, 'YYYY-MM-DD'), 'YYYY-MM-DD')
            as session_date,
            extract(epoch from (t.date_end::timestamp - t.date::timestamp)) /
            3600 as planned_hours,
            t.duration as real_hours,
            r.student_id as student_id,
            part.name as student_name,
            r.partner_id as customer_id,
            part2.name as customer_name
        """
        return select_

    def _from_event_attendace_report(self):
        from_ = """
            event_track t
            inner join event_track_stage st on st.id = t.stage_id
            inner join event_event e on e.id = t.event_id
            inner join event_registration r on r.event_id = t.event_id
            inner join res_partner part on part.id = r.student_id
            inner join res_partner part2 on part2.id = r.partner_id
            """
        return from_

    def _where_event_attendace_report(self):
        where_ = """
                 (st.is_cancel = True or st.is_done = True)
                 and r.student_id is not null
                 and r.real_date_start is not null
                 and to_date(to_char(t.date, 'YYYY-MM-DD'), 'YYYY-MM-DD') >=
                 r.real_date_start
                 and (r.real_date_end is null or
                 (r.real_date_end is not null
                 and to_date(to_char(t.date, 'YYYY-MM-DD'),'YYYY-MM-DD') <=
                 r.real_date_end))
                 """
        return where_

    def _order_by_event_attendace_report(self):
        order_by_ = """
                 part2.name, e.name,
                 to_date(to_char(t.date, 'YYYY-MM-DD'), 'YYYY-MM-DD'),
                 part2.name
                 """
        return order_by_

    def _query(self):
        return '(SELECT %s FROM %s WHERE %s ORDER BY %s)' % \
               (self._select_event_attendace_report(),
                self._from_event_attendace_report(),
                self._where_event_attendace_report(),
                self._order_by_event_attendace_report())

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" %
            (self._table, self._query()))
