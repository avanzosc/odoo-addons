# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestPurchaseOrderLineDescriptionFromSale(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.product_model = cls.env['product.product']
        cls.sale_model = cls.env['sale.order']
        cls.purchase_model = cls.env['purchase.order']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.partner = cls.partner_model.create({
            'name': 'Partner Test description from sale',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        cls.supplier = cls.partner_model.create({
            'name': 'Supplier Test description from sale',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        routes = cls.env.ref('stock.route_warehouse0_mto')
        routes += cls.env.ref('purchase_stock.route_warehouse0_buy')
        cls.product = cls.product_model.create({
            'name': 'Test description from sale',
            'type': 'product',
            'default_code': 'TDFS-test',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'route_ids': [(6, 0, routes.ids)],
            'variant_seller_ids': [(0, 0, {'name': cls.supplier.id})]
        })
        cls.product.categ_id.procured_purchase_grouping = 'line'
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
        }
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 5,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100,
        }
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        cls.sale_order = cls.sale_model.create(sale_vals)

    def test_purchase_line_description_from_sale(self):
        self.assertEquals(self.sale_order.state, 'draft')
        self.sale_order.order_line[0].name = 'Aaaaaaaaaa'
        self.sale_order.action_confirm()
        self.assertEquals(self.sale_order.state, 'sale')
        purchase = self.env['purchase.order'].search(
            [('partner_id', '=', self.supplier.id)], limit=1)
        self.assertEquals(len(purchase), 1)
        self.assertEquals(
            purchase.order_line[0].name, self.sale_order.order_line[0].name)
