# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    @api.constrains('license_plate', 'old_license_plate')
    def _check_applicant_duplicate(self):
        for record in self:
            if record.license_plate:
                cond = [('id', '!=', record.id), '|',
                        ('license_plate', 'ilike', record.license_plate),
                        ('old_license_plate', 'ilike', record.license_plate)]
                vehicle = record.env['fleet.vehicle'].search(cond, limit=1)
                if vehicle:
                    raise ValidationError(
                        _("The actual license plate is duplicated."))
            if record.old_license_plate:
                cond = [('id', '!=', record.id), '|',
                        ('license_plate', 'ilike', record.old_license_plate),
                        ('old_license_plate', 'ilike', (
                            record.old_license_plate))]
                vehicle = record.env['fleet.vehicle'].search(cond, limit=1)
                if vehicle:
                    raise ValidationError(
                        _("The first license plate is duplicated."))
