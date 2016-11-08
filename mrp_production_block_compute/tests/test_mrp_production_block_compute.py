# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpProductionBlockCompute(common.TransactionCase):

    def setUp(self):
        super(TestMrpProductionBlockCompute, self).setUp()
        self.mrp_production = self.env.ref('mrp.mrp_production_1')

    def test_block_compute(self):
        self.assertFalse(self.mrp_production.block)
        self.mrp_production.block_compute()
        self.assertTrue(self.mrp_production.block)
        self.mrp_production.block_compute()
        self.assertFalse(self.mrp_production.block)
