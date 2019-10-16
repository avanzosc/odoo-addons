# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields
from odoo.tests.common import SavepointCase


class TestPartnerCharacterization(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerCharacterization, cls).setUpClass()
        cls.today = fields.Date.today()
        cls.activity = cls.env['res.activity'].create({
            'name': 'Activity Name',
        })
        cls.activity_type1 = cls.env['res.activity.type'].create({
            'name': 'Type Name',
            'activity_id': cls.activity.id,
        })
        cls.economic_data = cls.env['res.partner.economic_data'].create({
            'partner_id': cls.env.ref('base.main_partner').id,
            'economic_date': cls.today,
        })

    def test_name_get(self):
        self.assertEqual(
            self.activity_type1.name_get()[0],
            (self.activity_type1.id, self.activity_type1.name))
        self.assertEqual(
            self.activity_type1.with_context(
                show_activity_name=True).name_get()[0],
            (self.activity_type1.id, '{} / {}'.format(
                self.activity_type1.activity_id.name,
                self.activity_type1.name)))
        current_year = fields.Date.from_string(self.today).year
        self.assertEqual(
            '[{}] {}'.format(current_year, self.economic_data.partner_id.name),
            self.economic_data.display_name)
