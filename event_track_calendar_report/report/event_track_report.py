# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields
from odoo import tools
from psycopg2 import sql


class EventTrackReport(models.Model):
    _name = 'event.track.report'
    _auto = False
    _description = 'Meetings and tracks in one calendar'

    meeting_id = fields.Many2one(
        string='Meeting', comodel_name='calendar.event')
    track_id = fields.Many2one(string='Track', comodel_name='event.track')
    name = fields.Char(string='Name')
    allday = fields.Boolean(string='All day', default=False)
    start = fields.Datetime(string='Start date')
    stop = fields.Datetime(string='Stop date')
    duration = fields.Float(string='Duration')
    user_id = fields.Many2one(string='Responsible', comodel_name='res.users')

    def init(self):
        query = """
SELECT
    id AS id,
    id AS meeting_id,
    null AS track_id,
    name,
    allday,
    start,
    stop,
    duration,
    user_id
FROM
    calendar_event
UNION ALL (
    SELECT
        event_track.id * -1 AS id,
        null AS meeting_id,
        event_track.id AS track_id,
        event_track.name,
        False AS allday,
        event_track.date AS start,
        event_track.date_end as stop,
        event_track.duration,
        res_users.id as user_id
    FROM
        event_track
        INNER JOIN res_users ON
            res_users.partner_id = event_track.partner_id)
"""
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table),
                sql.SQL(query)
            ))
