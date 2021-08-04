
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def get_partner_phase_slides(self, channel):

        partner_slides = None
        if (channel.content_view == 'phase' and
                channel.sudo().channel_partner_ids):
            partner_slide_info_ids = channel.sudo().slide_partner_ids.filtered(
                lambda i: i.partner_id.id == self.id
            )
            domain = [('channel_id', '=', channel.id),
                      ('is_preview', '!=', True)]
            if partner_slide_info_ids:
                info_slide_ids = partner_slide_info_ids.mapped(
                    'slide_id').sorted(key=lambda r: r.sequence)
                domain += [('sequence', '<=', info_slide_ids[-1].sequence)]
                limit = None
            else:
                search_ids = channel.slide_ids
                domain += [('id', 'in', search_ids.ids)]
                limit = 1

            show_slide_ids = self.env['slide.slide'].sudo().search(domain,
                order='sequence', limit=limit)

            if show_slide_ids:

                next_slide = self.get_partner_next_slide(show_slide_ids[-1],
                                                         channel)
                if next_slide:
                    show_slide_ids += next_slide

            partner_slides = show_slide_ids

        return partner_slides

    def get_partner_next_slide(self, slide_id, channel):
        next_slide = None

        partner_slide_info_id = channel.sudo().slide_partner_ids.filtered(
            lambda i: i.partner_id.id == self.id and
                      i.slide_id.id == slide_id.id
        )
        if partner_slide_info_id and partner_slide_info_id.completed:
            next_slide = self.env['slide.slide'].sudo().search([
                    ('channel_id', '=', channel.id),
                    ('is_preview', '!=', True),
                    ('sequence', '>', slide_id.sequence)],
                    order='sequence', limit=1)
        return next_slide
