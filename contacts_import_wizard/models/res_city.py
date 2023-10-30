# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCity(models.Model):
    _inherit = "res.city"

    def name_get(self):
        result = []
        for city in self:
            name = city.name
            if self.env.context.get('show_country_state', False):
                if city.state_id:
                    name = "%s (%s)" % (name, city.state_id.display_name)
                else:
                    name = "%s (%s)" % (name, city.country_id.display_name)
            result.append((city.id, name))
        return result
