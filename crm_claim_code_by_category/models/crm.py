# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.model
    def create(self, values):
        if values.get('code', '/') == '/':
            categ = self.env['crm.case.categ'].browse(values.get('categ_id'))
            if categ.sequence_id:
                values['code'] = (
                    categ.sequence_id.next_by_id(categ.sequence_id.id))
        return super(CrmClaim, self).create(values)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        if self.categ_id.sequence_id:
            default.setdefault('code', self.categ_id.sequence_id.next_by_id(
                self.categ_id.sequence_id.id))
        return super(CrmClaim, self).copy(default)


class CrmCaseCateg(models.Model):
    _inherit = 'crm.case.categ'

    sequence_id = fields.Many2one(
        comodel_name='ir.sequence', string='Sequence')
