# Copyright (c) 2022 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestVehicleLicensePlateUnique(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestVehicleLicensePlateUnique, cls).setUpClass()
        applicant_obj = cls.env['fleet.vehicle']
        cls.vehicle1 = applicant_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
            'license_plate': '1234JSG',
        })
        cls.vehicle2 = applicant_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
            'old_license_plate': '2345JAG',
        })
        cls.vehicle3 = applicant_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
        })
        cls.vehicle4 = applicant_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
        })

    def test_vehicle_license_plate_unique(self):
        with self.assertRaises(ValidationError):
            self.vehicle3.license_plate = self.vehicle1.license_plate
        with self.assertRaises(ValidationError):
            self.vehicle4.old_license_plate = self.vehicle2.old_license_plate
