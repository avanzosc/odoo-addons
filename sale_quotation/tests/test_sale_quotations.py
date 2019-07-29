# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions
from openerp import fields


class SaleQuotations(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleQuotations, cls).setUpClass()
        cls.sale_type = cls.env['sale.order.type'].create({
            'warehouse_id': cls.env['stock.warehouse'].search([], limit=1).id,
            'name': 'offer',
            'quotation_visible': True
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product to test'
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'upgrade': True,
            'order_line': [(0, 0, {'product_id': cls.product.id,
                                   'product_uom_qty': 100}, )],
            'type_id': cls.sale_type.id
        })

    def test_partials(self):
        date = fields.Datetime.now()
        self.assertEqual('Pending', self.sale_order.quotation_state)
        self.sale_order.quotation_confirmation_date = date
        self.assertEqual('Confirmed', self.sale_order.quotation_state)
        self.sale_order.quotation_confirmation_date = False
        self.sale_order.quotation_rejection_date = date
        self.assertEqual('Rejected', self.sale_order.quotation_state)
        with self.assertRaises(exceptions.ValidationError):
            self.sale_order.quotation_confirmation_date = date
