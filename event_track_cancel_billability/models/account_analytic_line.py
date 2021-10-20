# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    payable = fields.Float(
        string='Payable', compute='compute_payable', store=True)
    billable = fields.Float(
        string='Billable', compute='compute_billable', store=True)

    @api.depends('time_type_id')
    def compute_payable(self):
        types = self.env.ref('event_track_cancel_reason.time_type1')
        types |= self.env.ref('event_track_cancel_reason.time_type2')
        for track in self:
            track.payable = 0.0
            if track.time_type_id in types:
                track.payable = track.unit_amount

    @api.depends('time_type_id')
    def compute_billable(self):
        types = self.env.ref('event_track_cancel_reason.time_type1')
        types |= self.env.ref('event_track_cancel_reason.time_type2')
        types |= self.env.ref('event_track_cancel_reason.time_type3')
        for track in self:
            track.billable = 0.0
            if track.time_type_id in types:
                track.billable = track.unit_amount
