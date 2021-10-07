# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

fields_to_rename = [
    ('event.event', 'event_event', 'email_address', 'teacher_zoom_email'),
    ('event.event', 'event_event', 'password', 'teacher_zoom_pwd'),
    ('event.event', 'event_event', 'meeting_id', 'student_zoom_meetingid'),
    ('event.event', 'event_event', 'key', 'student_zoom_key'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, fields_to_rename)
