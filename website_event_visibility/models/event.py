
from odoo import api, fields, models
from datetime import datetime


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

    @api.onchange('date_begin', 'date_end')
    def compute_unpublish_website(self):
        today = datetime.today()
        for record in self:
            record.website_published = (record.date_begin <= today and record.date_end >= today)

    def cron_compute_unpublish_website(self):
        events = self.env['event.event'].search([
            ('website_published', '=', True)
        ])
        events.compute_unpublish_website()
