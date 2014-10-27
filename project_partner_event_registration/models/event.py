# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.one
    def assign_partners(self):
        registry_obj = self.env['event.registration']
        for partner in self.project_id.partners:
            if not registry_obj.search_count(
                    [('event_id', '=', self.id),
                     ('partner_id', '=', partner.id)]):
                registry_obj.create({
                    'partner_id': partner.id,
                    'event_id': self.id,
                    'name': partner.name,
                    'email': partner.email,
                    'phone': partner.phone,
                    'message_follower_ids': [
                        (4, partner.id),
                        (4, self.user_id.partner_id.id)]})
