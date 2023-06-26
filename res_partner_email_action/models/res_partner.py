# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_send_reset_password(self):
        users_obj = self.env['res.users']
        for res in self:
            partner_user = users_obj.search([('partner_id', '=', res.id)])
            if partner_user and partner_user.has_group('base.group_portal'):
                partner_user.reset_password(partner_user.email)
