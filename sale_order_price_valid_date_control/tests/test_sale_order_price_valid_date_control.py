# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class SaleOrder(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrder, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product to test',
            'price_valid_date': '1900-01-01 00:00:00'
        })
        cls.product2 = cls.env['product.product'].create({
            'name': 'Product2 to test',
            'price_valid_date': '1900-01-01 00:00:00'
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'upgrade': True,
            'order_line': [(0, 0, {'product_id': cls.product.id,
                                   'product_uom_qty': 100}, )],
        })

    def test_partials(self):
        with self.assertRaises(exceptions.ValidationError):
            self.sale_order.action_button_confirm()
        res = self.sale_order.order_line[0].product_id_change_with_wh(
            False,  self.product2.id, 0, False, 0, False, '',
            self.partner.id, False, True, False, False, False, False,
            False, context=None)
        self.assertEqual(res.get('warning') and True, True)
        self.assertEqual(res.get('warning')['message'],
                         u'The valid price date has expired: Product2 to test')
