# Copyright (c) 2020 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class FleetRouteStop(models.Model):
    _inherit = "fleet.route.stop"

    high_route_support_ids = fields.One2many(
        string='High tops', comodel_name='fleet.route.support',
        inverse_name='high_stop_id')
    low_route_support_ids = fields.One2many(
        string='Low tops', comodel_name='fleet.route.support',
        inverse_name='low_stop_id')

