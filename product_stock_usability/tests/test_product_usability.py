# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged

from .common import ProductUsabilityCommon


@tagged("post_install", "-at_install")
class TestProductUsability(ProductUsabilityCommon):
    def test_product_root_category(self):
        self.assertEqual(self.parent_category.root_category_id, self.parent_category)
        self.assertEqual(self.son_category.root_category_id, self.parent_category)
        self.son_category.write(
            {
                "parent_id": False,
            }
        )
        self.assertEqual(self.son_category.root_category_id, self.son_category)
