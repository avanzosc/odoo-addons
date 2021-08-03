# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestEventExtendedName(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventExtendedName, cls).setUpClass()
        cls.event = cls.env.ref('event.event_4')
        cls.calendar = cls.env.ref('resource.resource_calendar_std')
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.event.write({
            'resource_calendar_id': cls.calendar.id,
            'customer_id': cls.customer.id})

    def test_event_extenden_name(self):
        name = '{}'.format(self.event.id)
        if self.event.name:
            name = u'{} - {}'.format(name, self.event.name)
        if self.event.resource_calendar_id:
            name = u'{} - {}'.format(
                name, self.event.resource_calendar_id.name)
        if self.event.customer_id:
            name = u'{} - {}'.format(name, self.event.customer_id.name)
        if (self.event.address_id and
            (not self.event.customer_id or self.event.customer_id and
             self.event.customer_id != self.event.address_id)):
            name = u'{} - {}'.format(name, self.event.address_id.name)
        if (self.event.address_id and
            (self.event.address_id.street or self.event.address_id.street2 or
             self.event.address_id.zip or self.event.address_id.city)):
            name = u'{} -'.format(name)
            if self.event.address_id.street:
                name = u'{} {}'.format(name, self.event.address_id.street)
            if self.event.address_id.street2:
                name = u'{} {}'.format(name, self.event.address_id.street2)
            if self.event.address_id.zip:
                name = u'{} {}'.format(name, self.event.address_id.zip)
            if self.event.address_id.city:
                name = u'{} {}'.format(name, self.event.address_id.city)
        self.assertEqual(self.event.extended_name, name)
