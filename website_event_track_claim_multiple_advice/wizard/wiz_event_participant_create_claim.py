# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class WizEventRegistrationCancelParticipant(models.TransientModel):
    _inherit = 'wiz.event.participant.create.claim'

    def action_create_claim(self):
        self.ensure_one()
        claim_obj = self.env['crm.claim']
        result = super(
            WizEventRegistrationCancelParticipant, self).action_create_claim()
        partners = self.env['res.partner'].browse(
            self.env.context.get('active_ids'))
        if not self.categ_id.number_of_consecutive_fouls:
            return result
        for partner in partners:
            cond = [('categ_id', '=', self.categ_id.id),
                    ('partner_id', '=', partner.id),
                    ('event_id', '=', self.event_track_id.event_id.id),
                    ('event_track_id', '=', self.event_track_id.id)]
            claim = claim_obj.search(cond, limit=1)
            track = self.event_track_id.id
            tracks_names = self.event_track_id.name
            number = 1
            while (claim and number !=
                    self.categ_id.number_of_consecutive_fouls):
                track -= 1
                cond = [('categ_id', '=', self.categ_id.id),
                        ('partner_id', '=', partner.id),
                        ('event_id', '=', self.event_track_id.event_id.id),
                        ('event_track_id', '=', track)]
                claim = claim_obj.search(cond, limit=1)
                if claim:
                    tracks_names = u'{}, {}'.format(
                        tracks_names, claim.event_track_id.name)
                    number += 1
            if number == self.categ_id.number_of_consecutive_fouls:
                claim.send_to_responsible_notification_multiple_advice(
                    tracks_names)
        return result
