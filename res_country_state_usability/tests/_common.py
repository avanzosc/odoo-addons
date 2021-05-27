# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class ResCountryStateUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(ResCountryStateUsability, cls).setUpClass()
        country_obj = cls.env["res.country"]
        state_obj = cls.env["res.country.state"]
        cls.country = country_obj.create({
            "name": "Test Country",
            "code": "test",
        })
        cls.state_1 = state_obj.create({
            "name": "Test State 1",
            "country_id": cls.country.id,
            "code": "01",
        })
        cls.state_2 = state_obj.create({
            "name": "Test State 2",
            "country_id": cls.country.id,
            "code": "02",
        })
