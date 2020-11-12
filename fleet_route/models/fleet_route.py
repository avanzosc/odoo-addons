# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import re
from odoo import _, api, fields, models
from odoo.osv import expression


class FleetRoute(models.Model):
    _name = "fleet.route"
    _description = "Route"
    _order = "name_id,direction"

    route_code = fields.Char(
        string="Route code", readonly="1", index=True,
        default=lambda self: _("New"), copy=False)
    name_id = fields.Many2one(
        comodel_name="fleet.route.name", string="Route Name", required=True)
    abbreviation = fields.Char(
        string="Abbreviation")
    colour = fields.Char(
        string="Colour")
    vehicle_id = fields.Many2one(
        string="Vehicle", comodel_name="fleet.vehicle")
    vehicle_driver_ids = fields.Many2many(
        comodel_name="res.partner", string="Drivers",
        related="vehicle_id.driver_ids")
    vehicle_company_id = fields.Many2one(
        string="Vehicle's Company", comodel_name="res.company",
        related="vehicle_id.company_id")
    driver_id = fields.Many2one(
        string="Driver", comodel_name="res.partner")
    driver_commercial_id = fields.Many2one(
        comodel_name="res.partner", string="Driver's Commercial Entity",
        related="driver_id.commercial_partner_id")
    seats = fields.Integer(
        string="Seats", related="vehicle_id.seats")
    manager_id = fields.Many2one(
        string="Manager", comodel_name="hr.employee")
    manager_phone_mobile = fields.Char(
        string="Phone/mobile",
        compute="_compute_manager_phone_mobile", store=True)
    substitute_ids = fields.Many2many(
        comodel_name="hr.employee", relation="rel_route_employee",
        string="Substitutes")
    timetable = fields.Many2one(
        string="Timetable", comodel_name="resource.calendar")
    stop_ids = fields.One2many(
        string="Stops", comodel_name="fleet.route.stop",
        inverse_name="route_id")
    direction = fields.Selection(
        selection=[("going", "Going"),
                   ("coming", "Coming")], default="going", required=True)
    company_id = fields.Many2one(
        comodel_name="res.company", required=True, string="Company",
        default=lambda self: self.env["res.company"]._company_default_get(
            "fleet.route"))

    @api.depends("manager_id", "manager_id.work_phone",
                 "manager_id.mobile_phone")
    def _compute_manager_phone_mobile(self):
        for route in self:
            route.manager_phone_mobile = (
                route.manager_id and
                route.manager_id.get_employee_contact_info() or
                _("Not available"))

    @api.onchange("vehicle_id")
    def onchange_vehicle_id(self):
        for record in self:
            vehicle = record.vehicle_id
            if vehicle.driver_id:
                record.driver_id = vehicle.driver_id
            elif len(vehicle.driver_ids) == 1:
                record.driver_id = vehicle.driver_ids[:1]

    @api.model
    def create(self, values):
        if values.get("route_code", _("New")) == _("New"):
            values["route_code"] = (
                self.env["ir.sequence"].next_by_code("fleet.route") or
                _("New"))
        return super(FleetRoute, self).create(values)

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
            field = record._fields["direction"]
            direction = field.convert_to_export(record["direction"], record)
            result.append((record.id, "[{}] {} ({})".format(
                record.route_code, record.name_id.name, direction)))
        return result

    @api.model
    def _name_search(
            self, name="", args=None, operator="ilike", limit=100,
            name_get_uid=None):
        args = args or []
        route_ids = []
        fleet_name_obj = self.env["fleet.route.name"]
        if operator not in expression.NEGATIVE_TERM_OPERATORS:
            name_ids = fleet_name_obj._search(
                expression.AND([[("name", operator, name)], args]),
                limit=limit, access_rights_uid=name_get_uid)
            route_ids = self._search([("name_id", "in", name_ids)])
        if not route_ids:
            return super(FleetRoute, self)._name_search(
                name=name, args=args, operator=operator, limit=limit,
                name_get_uid=name_get_uid)
        return self.browse(route_ids).name_get()

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return re.sub(r"[\W_]+", "", self.display_name)
