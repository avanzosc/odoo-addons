# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('category_id')
    def _compute_label_id(self):
        for partner in self:
            partner.partner_label_id = (
                min(partner.category_id, key=lambda x: x.id) if
                partner.category_id else [])

    partner_label_id = fields.Many2one(
        comodel_name='res.partner.category', string='Label', store=True,
        compute='_compute_label_id')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        res = super(ResPartner, self).name_search(
            name, args=args, operator=operator, limit=limit)
        partners = self.browse([x[0] for x in res])
        if name and not partners:
            partners = self.search([('ref', operator, name)] + args,
                                   limit=limit)
        if name and not partners:
            partners = self.search([('vat', operator, name)] + args,
                                   limit=limit)
        return partners.name_get()
