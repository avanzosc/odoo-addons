# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestProductSupplierinfoView(common.TransactionCase):

    def setUp(self):
        super(TestProductSupplierinfoView, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        supplier = self.env['res.partner'].create({
            'name': 'Supplier for tests',
            'supplier': True,
        })
        product_tmpl = self.env['product.template'].create({
            'name': 'Template for tests',
        })
        self.suppinfo = self.supplierinfo_model.create({
            'name': supplier.id,
            'product_tmpl_id': product_tmpl.id,
            'pricelist_ids': [
                (0, 0, {'min_quantity': 1.0, 'price': 10.0}),
                (0, 0, {'min_quantity': 5.0, 'price': 5.0})],
        })

    def test_product_supplierinfo_prices(self):
        data = []
        for partnerinfo in self.suppinfo.pricelist_ids.sorted(
                lambda r: r.min_quantity):
            data.append("[{:.2f}] {:.2f}".format(partnerinfo.min_quantity,
                                                 partnerinfo.price))
        self.assertEqual(self.suppinfo.prices, ' // '.join(data))
