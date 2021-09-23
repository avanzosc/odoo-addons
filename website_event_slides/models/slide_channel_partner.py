from odoo import api, fields, models
from datetime import date


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    show_channel_partner = fields.Boolean(
        string='Show channel', compute='_compute_show_channel_partner',
        store=True)

    @api.depends("real_date_start", "real_date_end")
    def _compute_show_channel_partner(self):
        for record in self:
            show_partner = False
            if (record.real_date_start is False or record.real_date_start <= date.today()) and (record.real_date_end is False or date.today() <= record.real_date_end):
                show_partner = True
            record.show_channel_partner = show_partner
