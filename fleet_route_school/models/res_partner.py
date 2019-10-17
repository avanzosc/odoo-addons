# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = 'res.partner'

    stop_count = fields.Integer(compute='_compute_stop_count')

    @api.multi
    def _compute_stop_count(self):
        stop_obj = self.env['fleet.route.stop.passenger']
        for partner in self:
            partner.stop_count = stop_obj.search_count([
                ('partner_id', '=', partner.id)])

    @api.multi
    def button_open_partner_stops(self):
        action = self.env.ref('fleet_route.action_fleet_route_stop')
        action_dict = action.read()[0] if action else {}
        passenger_stops = self.env['fleet.route.stop.passenger'].search([
            ('partner_id', 'in', self.ids)])
        domain = expression.AND([
            [('id', 'in', passenger_stops.mapped('stop_id').ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
