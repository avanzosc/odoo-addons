# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestProductPricelistItemMenu(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_product_pricelist_item_menu1(self):
        partners = self.partner_model.search([])
        for partner in partners:
            self.assertEqual(
                partner.count_pricelists_item,
                len(partner.property_product_pricelist.item_ids),
            )

    def test_product_pricelist_item_menu2(self):
        partner = self.partner_model.search([], limit=1)
        res = partner.button_show_partner_pricelist_items()
        self.assertEqual(res.get("name"), "Pricelist Items")
        cond = [("pricelist_id", "=", partner.property_product_pricelist.id)]
        self.assertEqual(res.get("domain"), cond)
