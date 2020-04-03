# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStopPassenger(models.Model):
    _name = 'fleet.route.stop.passenger'
    _description = 'Passenger'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Passenger', required=True)
    stop_id = fields.Many2one(
        comodel_name='fleet.route.stop', string='Route Stop', required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    direction = fields.Selection(
        string="Direction", related="stop_id.direction", store=True)
    notes = fields.Text()
    estimated_time = fields.Float(
        string='Estimated time',
        related='stop_id.estimated_time', store=True)
    route_id = fields.Many2one(
        comodel_name='fleet.route', related='stop_id.route_id',
        string='Route', store=True)
    route_abbreviation = fields.Char(
        string='Abbreviation', related='stop_id.route_id.abbreviation',
        store=True)
    going_manager_id = fields.Many2one(
        string='Going Manager', comodel_name='hr.employee',
        related='stop_id.route_id.going_manager_id', store=True)
    going_manager_phone_mobile = fields.Char(
        string='Phone/mobile (Going)',
        related='stop_id.route_id.going_manager_phone_mobile', store=True)
    coming_manager_id = fields.Many2one(
        string='Coming Manager', comodel_name='hr.employee',
        related='stop_id.route_id.coming_manager_id', store=True)
    coming_manager_phone_mobile = fields.Char(
        string='Phone/mobile (Coming)',
        related='stop_id.route_id.coming_manager_phone_mobile', store=True)
    dayofweek_ids = fields.Many2many(
        comodel_name="fleet.route.stop.weekday", string="Days of Week",
        relation="res_fleet_route_stop_passenger_weekday",
        column1="passenger_id", column2="weekday_id")

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, '{} [{}-{}]'.format(
                record.partner_id.display_name, record.route_id.name,
                record.stop_id.name)))
        return result
