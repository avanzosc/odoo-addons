# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from ._common import ResCountryStateUsability
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestResCountryStateUsability(ResCountryStateUsability):

    def test_archive_unarchive_country(self):
        self.assertTrue(self.country.active)
        self.assertTrue(all(self.country.mapped("state_ids.active")))
        self.assertTrue(self.state_1.active)
        self.assertTrue(self.state_2.active)
        self.country.toggle_active()  # archive country
        self.assertFalse(self.country.active)
        self.assertFalse(self.state_1.active)
        self.assertFalse(self.state_2.active)
        self.country.toggle_active()  # unarchive country
        self.assertTrue(self.country.active)
        self.assertFalse(self.state_1.active)
        self.assertFalse(self.state_2.active)

    def test_archive_unarchive_state(self):
        self.assertTrue(self.country.active)
        self.assertTrue(all(self.country.mapped("state_ids.active")))
        self.assertTrue(self.state_1.active)
        self.assertTrue(self.state_2.active)
        self.state_1.toggle_active()  # archive state
        self.assertTrue(self.country.active)
        self.assertFalse(self.state_1.active)
        self.assertTrue(self.state_2.active)
        self.country.toggle_active()   # archive country
        self.assertFalse(self.country.active)
        self.assertFalse(self.state_1.active)
        self.assertFalse(self.state_2.active)
        self.state_1.toggle_active()   # unarchive state
        self.assertTrue(self.country.active)
        self.assertTrue(self.state_1.active)
        self.assertFalse(self.state_2.active)
