# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestMachineManager(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.machine1 = self.env.ref("machine_manager.machinery_1")

    def test_machine_manager_count(self):
        self.product1 = self.machine1.product_id
        self.assertEqual(
            len(self.product1.machine_ids),
            self.product1.machine_count,
            "Computed field is failing",
        )

    def test_machinery_company(self):
        self.assertEqual(
            self.env.user.company_id.id,
            self.machine1.company_id.id,
            "Companies do not match",
        )
