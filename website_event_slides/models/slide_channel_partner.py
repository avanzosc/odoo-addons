from odoo import api, fields, models


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    show_channel_partner = fields.Boolean(
        string="Show channel",
        compute="_compute_show_channel_partner",
        search="_search_show_channel_partner"
     )

    @api.depends("real_date_start", "real_date_end")
    def _compute_show_channel_partner(self):
        today = fields.Date.context_today(self)
        for record in self:
            record.show_channel_partner = (
                (record.real_date_start is False or record.real_date_start <= today)
                and (record.real_date_end is False or today <= record.real_date_end))

    @api.multi
    def _search_show_channel_partner(self, operator, value):
        today = fields.Date.context_today(self)
        channel_partner = self.search(
            ["&",
             "|", ("real_date_start", "=", False), ("real_date_start", "<=", today),
             "|", ("real_date_end", "=", False), ("real_date_end", ">=", today)])
        if operator == "=" and value:
            return [("id", "in", channel_partner.ids)]
        else:
            return [("id", "not in", channel_partner.ids)]
