
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    create_student_user_check = fields.Boolean(
        "Create user for student attendee",
        help="Create Portal User for event student.")
    create_student_check = fields.Boolean(
        "Create student partner",
        help="The Reserved by is not the one attending the event. "
             "Creates new partner for Student field.")
    generate_student_email_check = fields.Boolean(
        "Generate student email",
        help="Generate the Student an email at confirm if not set.")
