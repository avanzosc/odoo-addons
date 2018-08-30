# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class ResActivityType(models.Model):
    _inherit = 'res.activity.type'

    @api.multi
    def name_get(self):
        if not self.env.context.get('show_activity_name'):
            return super(ResActivityType, self).name_get()
        return [(value.id,
                 "{} / {}".format(value.activity_id.name, value.name))
                for value in self]
