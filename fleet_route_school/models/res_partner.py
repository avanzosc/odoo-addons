# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # bus_passenger = fields.Selection(
    #     selection=[("yes", "Yes"),
    #                ("no", "No")], string="Uses Bus")
    stop_ids = fields.One2many(
        comodel_name="fleet.route.stop.passenger", inverse_name="partner_id",
        string="Route Stop")
    stop_count = fields.Integer(
        compute='_compute_stop_count', string="# Route Stop", store=True,
        compute_sudo=True)

    @api.multi
    def write(self, values):
        result = super(ResPartner, self).write(values)
        if values.get("bus_passenger") == "no":
            self.stop_ids.filtered(lambda s: not s.end_date).write({
                "end_date": fields.Date.context_today(self),
            })
        return result

    @api.multi
    @api.depends("stop_ids")
    def _compute_stop_count(self):
        for partner in self:
            partner.stop_count = len(partner.stop_ids)

    @api.multi
    def button_open_partner_stops(self):
        self.ensure_one()
        action = self.env.ref(
            'fleet_route_school.action_fleet_route_stop_passenger')
        action_dict = action.read()[0] if action else {}
        passenger_stops = self.env['fleet.route.stop.passenger'].search([
            ('partner_id', 'in', self.ids)])
        domain = expression.AND([
            [('id', 'in', passenger_stops.ids)],
            safe_eval(action.domain or '[]')])
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'search_default_partner_id': self.id,
            'default_partner_id': self.id,
        })
        action_dict.update({
            'domain': domain,
        })
        return action_dict
