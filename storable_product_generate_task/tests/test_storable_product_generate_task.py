# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestStorableProductGenerateTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStorableProductGenerateTask, cls).setUpClass()
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner for storable product generate task',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product for storable product generate task',
            'default_code': 'Pfspgt',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'product',
            'service_tracking': 'task_new_project'
        })
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)]}
        cls.sale = cls.env['sale.order'].create(sale_vals)

    def test_storable_product_generate_task(self):
        self.sale.action_confirm()
        self.assertEqual(self.sale.tasks_count, 1)
        self.assertEqual(self.sale.tasks_ids[0].name, self.product.name)
