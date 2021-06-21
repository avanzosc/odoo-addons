# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestFleetExtension(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestFleetExtension, cls).setUpClass()
        cls.vehicle_obj = cls.env['fleet.vehicle']
        cls.serial_number_obj = cls.env['stock.production.lot']
        cls.serial_number1 = cls.serial_number_obj.create({
            'name': 'aaa',
            'product_id': cls.env['product.product'].search(
                [], limit=1).id,
            'company_id': cls.env['res.company'].search([], limit=1).id
        })
        cls.vehicle1 = cls.vehicle_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id,
            'license_plate': '2-ABC-001',
            'old_license_plate': '3-DEF-999',
            'serial_number_id': cls.serial_number1.id
            })
        cls.vehicle2 = cls.vehicle_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id
            })
        cls.serial_number2 = cls.serial_number_obj.create({
            'name': 'bbb',
            'product_id': cls.env['product.product'].search(
                [], limit=1).id,
            'company_id': cls.env['res.company'].search([], limit=1).id,
            'vehicle_id': cls.vehicle2.id})
        cls.vehicle3 = cls.vehicle_obj.create({
            'model_id': cls.env['fleet.vehicle.model'].search([], limit=1).id
            })
        cls.serial_number3 = cls.serial_number_obj.create({
            'name': 'ccc',
            'product_id': cls.env['product.product'].search(
                [], limit=1).id,
            'company_id': cls.env['res.company'].search([], limit=1).id
        })

    def test_fleet_extension(self):
        self.assertEqual(self.serial_number1.vehicle_id.id, self.vehicle1.id)
        self.assertEqual(
            self.vehicle2.serial_number_id.id, self.serial_number2.id)
        self.serial_number1.vehicle_id = self.vehicle3.id
        self.assertEqual(self.vehicle1.serial_number_id.id, False)
        self.vehicle2.serial_number_id = self.serial_number3.id
        self.assertEqual(self.serial_number2.vehicle_id.id, False)
        vehicles_found = self.vehicle_obj.name_search('2-ABC-001')
        self.assertEqual(len(vehicles_found), 1)
        self.assertEqual(vehicles_found[0][0], self.vehicle1.id)
        vehicles_found = self.vehicle_obj.name_search('3-DEF-999')
        self.assertEqual(len(vehicles_found), 1)
        self.assertEqual(vehicles_found[0][0], self.vehicle1.id)
        domain = ['|',
                  ['name', 'ilike', '2-ABC-001'],
                  ['license_plate', 'ilike', '2-ABC-001']]
        vehicles_found = self.vehicle_obj.search_read(domain)
        self.assertEqual(len(vehicles_found), 1)
        self.assertEqual(vehicles_found[0]['id'], self.vehicle1.id)
        domain = ['|',
                  ['name', 'ilike', '3-DEF-999'],
                  ['license_plate', 'ilike', '3-DEF-999']]
        vehicles_found = self.vehicle_obj.search_read(domain)
        self.assertEqual(len(vehicles_found), 1)
        self.assertEqual(vehicles_found[0]['id'], self.vehicle1.id)
