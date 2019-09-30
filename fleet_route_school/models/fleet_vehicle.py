# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    center_ids = fields.Many2many(
        comodel_name='res.partner', string='Education Centers')
