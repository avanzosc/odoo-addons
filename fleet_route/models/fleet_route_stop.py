# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class FleetRouteStop(models.Model):
    _name = 'fleet.route.stop'
    _description = 'Route Stop'

    name = fields.Char(string='Description', required=True)
    location_id = fields.Many2one(
        string='Location', comodel_name='res.partner',
        domain=lambda self: [
            ('category_id', 'in',
             self.env.ref('fleet_route.stop_location_partner_cat').id)])
    street = fields.Char(
        string='Street', related='location_id.street')
    city = fields.Char(
        string='City', related='location_id.city')
    state_id = fields.Many2one(
        string='State', comodel_name='res.country.state',
        related='location_id.state_id')
    country_id = fields.Many2one(
        string='Country', comodel_name='res.country',
        related='location_id.country_id')
    comment = fields.Text(
        string='Internal notes', related='location_id.comment')
    departure_estimated_time = fields.Float(
        string='Departure estimated time')
    return_estimated_time = fields.Float(
        string='Return estimated time')
    route_id = fields.Many2one(
        string='Route', comodel_name='fleet.route', required=True,
        ondelete='cascade')
