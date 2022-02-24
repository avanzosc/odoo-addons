# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    partner_responsible_id = fields.Many2one(
        string='Responsible', related='event_responsible_id.partner_id',
        store=True)
    tracks_names = fields.Char(string='Sessions description')

    def send_to_responsible_notification_multiple_advice(self, tracks_names):
        mail_template = self.env.ref(
            "website_event_track_claim_multiple_advice.student_with_multiple"
            "_advice_mail")
        for claim in self:
            claim.tracks_names = tracks_names
            mail_template.send_mail(claim.id, force_send=True)
