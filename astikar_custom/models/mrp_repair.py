# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    def _defaul_quotation_notes(self):
        return self.env.user.company_id.sale_note

    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('mrp.repair') or '/'
        new_id = super(MrpRepair, self).create(vals)
        return new_id

    name = fields.Char(default=False, required=False)
    quotation_notes = fields.Text(default=_defaul_quotation_notes)
