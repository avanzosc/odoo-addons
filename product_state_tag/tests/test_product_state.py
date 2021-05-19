# Copyright (c) 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import UserError


class TestProductState(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductState, cls).setUpClass()
        cls.init_state = cls.env.ref('product_state_tag.product_first_state')

    def test_product_state(self):
        with self.assertRaises(UserError):
            self.init_state.unlink()
