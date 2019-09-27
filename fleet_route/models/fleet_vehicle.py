# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    driver_commercial_partner_id = fields.Many2one(
        comodel_name='res.partner', string='Driver\'s Commercial Entity',
        related='driver_id.commercial_partner_id', store=True)
