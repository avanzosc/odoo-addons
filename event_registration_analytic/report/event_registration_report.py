# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, tools


class EventRegistrationReport(models.Model):
    _name = 'event.registration.report'
    _description = 'Report with counters for event registrations'
    _auto = False
    _order = ('address_id, event_id, date')

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Center', readonly=True)
    event_id = fields.Many2one(
        comodel_name='event.event', string='Event', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    high_counter = fields.Integer(string='Highs', readonly=True)
    down_counter = fields.Integer(string='Downs', readonly=True)
    number_records_total = fields.Integer(
        string='Number records total', readonly=True)
    unsubscribe_requests_counter = fields.Integer(
        string='Unsubscribe requests', readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'event_registration_report')
        cr.execute("""
        CREATE OR REPLACE VIEW event_registration_report AS (
       select cast(cast(ev.id as varchar) ||
              to_char(evday.edate,'YYMM') as integer) as id,
              ev.address_id as address_id, ev.id as event_id,
              to_date(to_char(evday.edate,'YYYY-MM-') || extract (day from (
                     select date_trunc('month',
                     to_date(to_char(evday.edate,'YYYYMM'), 'YYYYMM')) +
                     '1month' ::interval -'1sec' ::interval)),
                     'YYYY-MM-DD') as date,
              (select count(*)
               from event_registration
               where event_id = ev.id and
                     state != 'draft' and
                     employee is null and
                     to_char(date_start,'YYYY-MM') =
                     to_char(evday.edate,'YYYY-MM')) as high_counter,
              (select count(*)
               from event_registration
               where event_id = ev.id and
                     state != 'draft' and
                     employee is null and
                     to_char(date_end,'YYYY-MM') =
                     to_char(evday.edate,'YYYY-MM')) as down_counter,
              (select count(*)
               from event_registration
               where event_id = ev.id and
                     state != 'draft' and
                     employee is null and
                     to_char(date_start,'YYYY-MM') <=
                     to_char(evday.edate,'YYYY-MM'))
                     -
              (select count(*)
               from event_registration
               where event_id = ev.id and
                     state != 'draft' and
                     employee is null and
                     to_char(date_end,'YYYY-MM') <=
                     to_char(evday.edate,'YYYY-MM')) as number_records_total,
              (select count(*)
               from event_registration
               where event_id = ev.id and
                     state != 'draft' and
                     employee is null and
                     to_char(removal_date,'YYYY-MM') = to_char(evday.edate,
                     'YYYY-MM')) as unsubscribe_requests_counter
        from event_event ev left join
        (select generate_series(e.date_begin::date,e.date_end::date,
        '1 month'::interval), e.id from event_event e) as evday(edate, e)
        on e=ev.id
       group by 1, 2, 3, 4, 5, 6, 7, 8
       order by 2, 3, 4)""")
