# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields


@common.at_install(False)
@common.post_install(True)
class TestPurchaseOrderLineWithTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseOrderLineWithTask, cls).setUpClass()
        cls.invoice_obj = cls.env["account.invoice"]
        cls.uom_unit = cls.env.ref("product.product_uom_unit")
        cls.project = cls.env["project.project"].create({
            "name": "Project Purchase Order Line With Task",
        })
        cls.task = cls.env["project.task"].create({
            "name": "Task 1 Purchase Order Line With Task",
            "project_id": cls.project.id})
        cls.supplier = cls.env["res.partner"].create({
            "name": "Supplier Purchase Order Line With Task",
            "supplier": "True",
        })
        cls.product = cls.env["product.product"].create({
            "name": "Product Purchase Order Line With Task",
            "type": "product",
            "default_code": "PPOLWT",
            "uom_id": cls.uom_unit.id,
            "uom_po_id": cls.uom_unit.id
        })
        cls.purchase = cls.env["purchase.order"].create({
            "partner_id": cls.supplier.id,
            "order_line": [
                (0, 0, {
                    "name": cls.product.name,
                    "product_id": cls.product.id,
                    "product_qty": 10.0,
                    "product_uom": cls.product.uom_po_id.id,
                    "price_unit": cls.product.standard_price,
                    "date_planned": fields.Datetime.now(),
                    "account_analytic_id": cls.project.analytic_account_id.id
                })],
        })
        cls.purchase_line = cls.purchase.order_line[0]

    def test_purchase_order_line_with_task(self):
        self.purchase_line.onchange_account_analytic_id()
        self.assertEqual(
            len(self.purchase_line.allowed_task_ids), 1)
        self.assertEqual(self.purchase_line.task_id, self.task)
        self.assertEqual(self.task.purchase_count, 1)
        self.assertEqual(self.task.purchase_line_count, 1)
        invoice_vals = {
            "partner_id": self.supplier.id,
            "purchase_id": self.purchase.id}
        invoice = self.invoice_obj.create(invoice_vals)
        invoice.purchase_order_change()
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        invoice_line = invoice.invoice_line_ids[0]
        self.assertEqual(
            len(invoice_line.allowed_task_ids), 1)
        self.assertEqual(invoice_line.task_id, self.task)
        self.assertEqual(self.task.purchase_invoice_count, 1)
        self.assertEqual(self.task.purchase_invoice_line_count, 1)
        invoice.action_invoice_open()
