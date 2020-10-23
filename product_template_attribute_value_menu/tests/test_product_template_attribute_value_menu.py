# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestProductTemplateAttributeValueMenu(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductTemplateAttributeValueMenu, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.value_model = cls.env['product.template.attribute.value']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product = cls.product_model.create({
            'name': 'Product_1',
            'type': 'product',
            'default_code': 'P123457',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        value = cls.value_model.search([], limit=1)
        cls.new_value = value.copy(
            default={"product_tmpl_id": cls.product.product_tmpl_id.id})
        cls.product.attribute_value_ids = [
            (6, 0, cls.new_value.product_attribute_value_id.ids)]

    def test_product_template_attribute_value_menu(self):
        quantity_on_hand = (
            self.product.qty_available - self.product.outgoing_qty)
        self.assertEquals(self.new_value.quantity_on_hand, quantity_on_hand)
