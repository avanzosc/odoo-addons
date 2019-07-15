# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class SaleOrderPartials(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrderPartials, cls).setUpClass()
        cls.attachment = cls.env['duplicate.upgradable.sale']
        cls.attachment = cls.env['ir.attachment'].create({
            'res_model': 'product.product',
            'res_id': '1'
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product to test'
        })

    def test_partials(self):
        self.assertEqual(self.product.attachment_qty, 1)
