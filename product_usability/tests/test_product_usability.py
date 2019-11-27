# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import ProductUsability
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestProductUsability(ProductUsability):

    def test_product_root_category(self):
        self.assertEquals(
            self.parent_category.root_category_id, self.parent_category)
        self.assertEquals(
            self.son_category.root_category_id, self.parent_category)
        self.son_category.write({
            'parent_id': False,
        })
        self.assertEquals(
            self.son_category.root_category_id, self.son_category)
