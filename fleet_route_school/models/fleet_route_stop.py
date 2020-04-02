# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStop(models.Model):
    _inherit = 'fleet.route.stop'

    passenger_ids = fields.One2many(
        comodel_name='fleet.route.stop.passenger', inverse_name='stop_id',
        string='Passengers')
    passenger_count = fields.Integer(
        string="Passenger Count", compute='_compute_passenger_count',
        store=True)
    route_abbreviation = fields.Char(
        string='Abbreviation', related='route_id.abbreviation',
        store=True)
    going_manager_id = fields.Many2one(
        string='Going Manager', comodel_name='hr.employee',
        related='route_id.going_manager_id', store=True)
    going_manager_phone_mobile = fields.Char(
        string='Phone/mobile (Going)',
        related='route_id.going_manager_phone_mobile', store=True)
    coming_manager_id = fields.Many2one(
        string='Coming Manager', comodel_name='hr.employee',
        related='route_id.coming_manager_id', store=True)
    coming_manager_phone_mobile = fields.Char(
        string='Phone/mobile (Coming)',
        related='route_id.coming_manager_phone_mobile', store=True)

    @api.multi
    @api.depends("passenger_ids", "passenger_ids.partner_id")
    def _compute_passenger_count(self):
        for stop in self:
            stop.passenger_count = len(stop.mapped("passenger_ids.partner_id"))
