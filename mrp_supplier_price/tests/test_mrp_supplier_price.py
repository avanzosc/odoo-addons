# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class MrpSupplierPriceTest(TransactionCase):

    def setUp(self):
        super(MrpSupplierPriceTest, self).setUp()
        self.mrp_production_model = self.env['mrp.production']
        self.bom_model = self.env['mrp.bom']
        self.product_model = self.env['product.product']
        unit_id = self.ref('product.product_uom_unit')
        dozen_id = self.ref('product.product_uom_dozen')
        self.supplier = self.env['res.partner'].create({
            'name': 'Supplier Test',
            'supplier': True,
        })
        bom_product = self.product_model.create({
            'name': 'BoM product',
            'uom_id': unit_id,
        })
        self.component1 = self.product_model.create({
            'name': 'Component1',
            'standard_price': 10.0,
            'uom_id': dozen_id,
            'uop_id': unit_id,
            'uom_po_id': unit_id,
            'uop_coeff': 12.0,
        })
        self.component2 = self.product_model.create({
            'name': 'Component2',
            'standard_price': 15.0,
            'uom_id': unit_id,
            'uop_id': unit_id,
            'uom_po_id': unit_id,
            'uop_coeff': 1.0,
        })
        self.env['product.supplierinfo'].create({
            'name': self.supplier.id,
            'product_tmpl_id': self.component2.product_tmpl_id.id,
            'pricelist_ids': [(0, 0, {'min_quantity': 1.0, 'price': 10.0}),
                              (0, 0, {'min_quantity': 10.0, 'price': 8.0})]
        })
        vals = {
            'product_tmpl_id': bom_product.product_tmpl_id.id,
            'product_id': bom_product.id,
            'bom_line_ids':
                [(0, 0, {'product_id': self.component1.id,
                         'product_qty': 2.0}),
                 (0, 0, {'product_id': self.component2.id,
                         'product_qty': 12.0})],
        }
        self.mrp_bom = self.bom_model.create(vals)
        self.production = self.mrp_production_model.create({
            'product_id': bom_product.id,
            'product_uom': bom_product.uom_id.id,
            'bom_id': self.mrp_bom.id,
        })

    def test_mrp_production(self):
        self.production.action_compute()
        self.assertEquals(len(self.production.bom_id.bom_line_ids),
                          len(self.production.product_lines))
        self.assertEquals(len(self.mrp_bom.bom_line_ids),
                          len(self.production.product_lines))
        self.assertEquals(
            self.production.scheduled_total,
            sum(self.production.mapped('product_lines.subtotal')))
        try:
            self.assertEquals(
                self.production.production_total,
                self.production.scheduled_total +
                self.production.routing_total)
        except:
            self.assertEquals(
                self.production.production_total,
                self.production.scheduled_total)
        for line in self.production.product_lines:
            self.assertEquals(
                line.uop_qty, line.product_qty * line.product_id.uop_coeff)
            self.assertEquals(
                line.uop_id,
                line.product_id.uop_id or line.product_id.uom_po_id)
            line.onchange_product_product_qty()
            self.assertEquals(round(line.uop_price, 2),
                              round(line.cost / line.product_id.uop_coeff, 2))
            self.assertEquals(round(line.subtotal, 2),
                              round(line.cost * line.product_qty, 2))
