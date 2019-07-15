# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, values):
        for partner in self:
            if (('parent_id' in values and partner.parent_id and
                 partner.parent_id.id != values.get('parent_id')) and
                    not self.env.context.get('change_parent')):
                raise exceptions.Warning(
                    _('You can\'t change the parent, please use the wizard.'))
            super(ResPartner, partner).write(values)
        return True
