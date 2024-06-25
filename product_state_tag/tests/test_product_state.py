# Copyright (c) 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProductState(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.init_state = cls.env.ref("product_state_tag.product_first_state")

    def test_product_state(self):
        with self.assertRaises(UserError):
            self.init_state.unlink()
