# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


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
    driver_commercial_id = fields.Many2one(
        comodel_name='res.partner', string='Driver\'s Commercial Entity',
        related='driver_id.commercial_partner_id')
    seats = fields.Integer(
        string='Seats', related='vehicle_id.seats')
    manager_id = fields.Many2one(
        string='Manager', comodel_name='hr.employee', required=True)
    manager_phone_mobile = fields.Char(
        string='Phone/mobile', compute='_compute_manager_phone_mobile',
        store=True)
    substitute_ids = fields.Many2many(
        comodel_name='hr.employee', relation='rel_route_employee',
        string='Substitutes')
    timetable = fields.Many2one(
        string='Timetable', comodel_name='resource.calendar')
    stop_ids = fields.One2many(
        string='Stops', comodel_name='fleet.route.stop',
        inverse_name='route_id')

    @api.depends('manager_id', 'manager_id.work_phone',
                 'manager_id.mobile_phone')
    def _compute_manager_phone_mobile(self):
        for route in self:
            route.manager_phone_mobile = (
                route.manager_id.get_employee_contact_info())

    @api.model
    def create(self, values):
        values['route_code'] = self.env['ir.sequence'].next_by_code(
            'fleet.route')
        return super(FleetRoute, self).create(values)
