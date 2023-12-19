# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class ProductUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(ProductUsability, cls).setUpClass()
        cls.category_model = cls.env['product.category']
        cls.parent_category = cls.category_model.create({
            'name': 'Test Parent Category',
        })
        cls.son_category = cls.category_model.create({
            'name': 'Test Son Category',
            'parent_id': cls.parent_category.id,
        })
