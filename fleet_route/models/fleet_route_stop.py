# Copyright 2019 Mentxu Isuskitza - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class FleetRouteStop(models.Model):
    _name = 'fleet.route.stop'
    _description = 'Route Stop'
    _order = 'route_id, sequence, estimated_time'

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
    estimated_time = fields.Float(string='Estimated time')
    sequence = fields.Integer(string="Sequence", default=1)
    route_id = fields.Many2one(
        string='Route', comodel_name='fleet.route', required=True,
        ondelete='cascade')
    manager_id = fields.Many2one(
        string="Manager", comodel_name="hr.employee",
        related="route_id.manager_id", store=True)
    manager_phone_mobile = fields.Char(
        string="Phone/mobile", related="route_id.manager_phone_mobile",
        store=True)

    @api.onchange("location_id")
    def _onchange_location_id(self):
        self.ensure_one()
        if not self.name:
            self.name = self.location_id.display_name

    @api.multi
    def open_map(self):
        self.ensure_one()
        return self.location_id.open_map()

    @api.multi
    def button_open_form(self):
        self.ensure_one()
        action = self.env.ref("fleet_route.action_fleet_route_stop")
        form_view = self.env.ref("fleet_route.fleet_route_stop_view_form")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
            "view_id": form_view.id,
            "view_mode": "form",
            "res_id": self.id,
            "views": [],
        })
        return action_dict

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        if self.env.context.get("hide_route"):
            return super(FleetRouteStop, self).name_get()
        for record in self:
            field = record.route_id._fields["direction"]
            direction = field.convert_to_export(
                record.route_id["direction"], record.route_id)
            result.append((record.id, "{} [{} ({})]".format(
                record.name, record.route_id.name_id.name, direction)))
        return result
