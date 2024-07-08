# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import odoo.tests.common as common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderLineInventory(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_line = cls.env["sale.order.line"].search([], limit=1)

    def test_sale_order_line_inventory(self):
        result = self.sale_line.show_product_inventory()
        context = result.get("context")
        lit = "'search_default_product_id': {}".format(self.sale_line.product_id.id)
        self.assertIn(lit, context)
