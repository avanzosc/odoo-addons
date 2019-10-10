# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestResourceBonus(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestResourceBonus, cls).setUpClass()
        cls.attendance_model = cls.env['resource.calendar.attendance']
        cls.attendance_dict = cls.attendance_model.default_get(
            cls.attendance_model.fields_get_keys())
        cls.bonus_model = cls.env['resource.calendar.bonus']
        cls.bonus_dict = cls.bonus_model.default_get(
            cls.bonus_model.fields_get_keys())

    def test_resource_bonus(self):
        self.assertEquals(
            self.bonus_dict.get('dayofweek'),
            self.attendance_dict.get('dayofweek'))
