
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    enroll = fields.Selection([
        ('public', 'Public'), ('invite', 'On Invitation')],
        default='public', string='Enroll Policy', required=True,
        help='Condition to enroll: everyone, on invite, '
             'on payment (sale bridge).')
    visibility = fields.Selection([
        ('public', 'Public'), ('members', 'Members Only')],
        default='public', string='Visibility', required=True,
        help='Applied directly as ACLs. Allow to hide channels'
             ' and their content for non members.')
