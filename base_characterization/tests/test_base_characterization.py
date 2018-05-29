# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestBaseCharacterization(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestBaseCharacterization, cls).setUpClass()
        cls.area_model = cls.env['res.area']
        cls.type_model = cls.env['res.area.type']

    def test_area_name_get(self):
        name = 'name'
        code = 'code'
        area = self.area_model.create({
            'name': name
        })
        self.assertTrue([(area.id, name)], area.name_get())
        area.write({
            'code': code,
        })
        new_name = '{}. {}'.format(code, name)
        self.assertTrue([(area.id, new_name)], area.name_get())

    def test_area_type_name_get(self):
        name = 'name'
        code = 'code'
        area_type = self.type_model.create({
            'name': name,
        })
        self.assertTrue([(area_type.id, name)], area_type.name_get())
        area_type.write({
            'code': code,
        })
        new_name = '{}. {}'.format(code, name)
        self.assertTrue([(area_type.id, new_name)], area_type.name_get())
