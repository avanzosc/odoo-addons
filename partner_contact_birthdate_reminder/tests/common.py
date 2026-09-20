# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common
from dateutil.relativedelta import relativedelta


class TestContactBirthdateCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContactBirthdateCommon, cls).setUpClass()
        cls.partner_obj = cls.env["res.partner"]
        cls.today = fields.Date.today()
        cls.bday_today = cls.partner_obj.create({
            "name": "Birthday is today",
            "birthdate_date": cls.today
        })
        new_partners = cls.partner_obj
        for days in range(1, 8):
            new_date = cls.today + relativedelta(days=days)
            new_partners |= cls.partner_obj.create({
                "name": "Bday is {}".format(new_date),
                "birthdate_date": new_date,
            })
