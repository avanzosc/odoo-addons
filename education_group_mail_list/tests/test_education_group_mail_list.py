# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestEducationGroupMailListCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestEducation(TestEducationGroupMailListCommon):

    def test_education_group(self):
        self.assertFalse(self.group.mail_list_ids)
        self.assertEquals(
            self.group.mail_list_count, len(self.group.mail_list_ids))
        action_dict = self.group.generate_lists()
        self.assertIn(
            ('group_id', 'in', self.group.ids), action_dict.get("domain"))
