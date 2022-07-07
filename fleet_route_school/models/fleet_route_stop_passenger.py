# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStopPassenger(models.Model):
    _name = "fleet.route.stop.passenger"
    _description = "Passenger"

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Passenger", required=True)
    stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="Route Stop", required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    notes = fields.Text()
    estimated_time = fields.Float(
        string="Estimated time",
        related="stop_id.estimated_time", store=True)
    route_id = fields.Many2one(
        comodel_name="fleet.route", related="stop_id.route_id",
        string="Route", store=True)
    route_abbreviation = fields.Char(
        string="Abbreviation", related="stop_id.route_id.abbreviation",
        store=True)
    manager_id = fields.Many2one(
        string="Manager", comodel_name="hr.employee",
        related="stop_id.route_id.manager_id", store=True)
    manager_phone_mobile = fields.Char(
        string="Phone/mobile",
        related="stop_id.route_id.manager_phone_mobile", store=True)
    dayofweek_ids = fields.Many2many(
        comodel_name="fleet.route.stop.weekday", string="Days of Week",
        relation="res_fleet_route_stop_passenger_weekday",
        column1="passenger_id", column2="weekday_id")
    route_name_id = fields.Many2one(
        comodel_name="fleet.route.name", related="stop_id.route_id.name_id",
        string="Route Name", store=True)
    route_timetable_id = fields.Many2one(
        comodel_name="resource.calendar",
        related="stop_id.route_id.timetable",
        string="Route Timetable",
        store=True,
    )
    possible_route_product_ids = fields.Many2many(
        comodel_name="product.product", string="Possible Invoicing Products",
        compute="_compute_possible_product_ids", store=True, compute_sudo=True)
    route_product_id = fields.Many2one(
        comodel_name="product.product", string="Invoicing Product")

    @api.multi
    @api.depends("stop_id", "stop_id.route_id", "stop_id.route_id.name_id",
                 "stop_id.route_id.name_id.complete_route_product_id",
                 "stop_id.route_id.name_id.half_route_product_id")
    def _compute_possible_product_ids(self):
        for passenger in self:
            route_name = passenger.stop_id.route_id.name_id
            passenger.possible_route_product_ids = [(6, 0, (
                route_name.complete_route_product_id |
                route_name.half_route_product_id).ids)]

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
            result.append((record.id, "{} [{}-{}]".format(
                record.partner_id.display_name, record.route_id.name_id.name,
                record.stop_id.name)))
        return result

    @api.multi
    def check_active(self, date=False):
        self.ensure_one()
        if not date:
            date = fields.Date.context_today(self)
        weekday = str(date.weekday())
        if ((((self.start_date and (self.start_date <= date)) or
             not self.start_date) and
                ((self.end_date and (self.end_date >= date)) or
                 not self.end_date)) and
                (not self.dayofweek_ids or
                 (weekday in self.dayofweek_ids.mapped("dayofweek")))):
            return True
        return False
