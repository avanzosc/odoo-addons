# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def get_state_name(self):
        name = ''
        if self.state_id:
            if '(' not in self.state_id.name:
                name = u'({})'.format(self.state_id.name)
            else:
                a = self.state_id.name.find('(')
                name = u'( {})'.format(self.state_id.name[:a])
        return name
