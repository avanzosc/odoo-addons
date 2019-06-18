# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class FleetItinerary(models.Model):
    _name = 'fleet.itinerary'
    _description = 'Itinerary'

    name = fields.Char(string='Description', required=True)
    stop_id = fields.Many2one(
        string='Stop', comodel_name='res.partner',
        domain=lambda self: [
            ('category_id', 'in',
             self.env.ref('fleet_route.stop_location_partner_cat').id)])
    street = fields.Char(
        string='Street', related='stop_id.street')
    city = fields.Char(
        string='City', related='stop_id.city')
    state_id = fields.Many2one(
        string='State', comodel_name='res.country.state',
        related='stop_id.state_id')
    country_id = fields.Many2one(
        string='Country', comodel_name='res.country',
        related='stop_id.country_id')
    comment = fields.Text(
        string='Internal notes', related='stop_id.comment')
    departure_estimated_time = fields.Float(
        string='Departure estimated time')
    return_estimated_time = fields.Float(
        string='Return estimated time')
    route_id = fields.Many2one(
        string='Route', comodel_name='fleet.route')


class FleetRoute(models.Model):
    _name = 'fleet.route'
    _description = 'Route'

    route_code = fields.Char(
        string='Route code', readonly="1")
    name = fields.Char(
        string='Name', required=True)
    abbreviation = fields.Char(
        string='Abbreviation')
    colour = fields.Char(
        string='Colour')
    vehicle_id = fields.Many2one(
        string='Vehicle', comodel_name='fleet.vehicle')
    company_id = fields.Many2one(
        string='Company', comodel_name='res.company',
        related='vehicle_id.company_id')
    driver_id = fields.Many2one(
        string='Driver', comodel_name='res.partner',
        related='vehicle_id.driver_id')
    seats = fields.Integer(
        string='Seats', related='vehicle_id.seats')
    manager_id = fields.Many2one(
        string='Manager', comodel_name='hr.employee')
    manager_phone_mobile = fields.Char(
        string='Phone/mobile', compute='_compute_manager_phone_mobile',
        store=True)
    substitute_id = fields.Many2one(
        string='Substitute manager', comodel_name='hr.employee')
    substitute_phone_mobile = fields.Char(
        string='Phone/mobile', compute='_compute_substitute_phone_mobile',
        store=True)
    timetable = fields.Many2one(
        string='Timetable', comodel_name='resource.calendar')
    itinerary_ids = fields.One2many(
        string='Itineraries', comodel_name='fleet.itinerary',
        inverse_name='route_id')

    @api.depends('manager_id', 'manager_id.work_phone',
                 'manager_id.mobile_phone')
    def _compute_manager_phone_mobile(self):
        for route in self.filtered(lambda c: c.manager_id):
            route.manager_phone_mobile = "{}/{}".format(
                route.manager_id.work_phone or '',
                route.manager_id.mobile_phone or '')

    @api.depends('manager_id', 'substitute_id.work_phone',
                 'substitute_id.mobile_phone')
    def _compute_substitute_phone_mobile(self):
        for route in self.filtered(lambda c: c.substitute_id):
            route.substitute_phone_mobile = "{}/{}".format(
                route.substitute_id.work_phone or '',
                route.substitute_id.mobile_phone or '')

    @api.model
    def create(self, values):
        values['route_code'] = self.env['ir.sequence'].next_by_code(
            'fleet.route')
        return super(FleetRoute, self).create(values)
