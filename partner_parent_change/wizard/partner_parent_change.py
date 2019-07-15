# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ResPartnerParentChange(models.TransientModel):
    _name = 'res.partner.parent.change'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner')
    old_parent_id = fields.Many2one(
        comodel_name='res.partner', string='Old Parent')
    new_parent_id = fields.Many2one(
        comodel_name='res.partner', string='New Parent',
        domain="[('is_company', '=', True), ('id', '!=', old_parent_id)]")

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(ResPartnerParentChange, self).default_get(fields_list)
        if 'active_id' in context:
            partner = self.env[context.get('active_model')].browse(
                context.get('active_id'))
            res.update({
                'partner_id': partner.id,
                'old_parent_id': partner.parent_id.id,
            })
        return res

    @api.multi
    def change_parent_id(self):
        self.ensure_one()
        reltype = self.env.ref('partner_parent_change.parent_relation_type')
        reltypesel = self.env['res.partner.relation.type.selection'].search(
            [('type_id', '=', reltype.id), ('is_inverse', '=', False)])
        today = fields.Date.context_today(self)
        relation_obj = self.env['res.partner.relation.all']
        relation = relation_obj.search([
            ('this_partner_id', '=', self.old_parent_id.id),
            ('other_partner_id', '=', self.partner_id.id)])
        if relation:
            relation.write({'date_end': today})
        else:
            relation_obj.create({
                'this_partner_id': self.old_parent_id.id,
                'type_selection_id': reltypesel.id,
                'other_partner_id': self.partner_id.id,
                'date_end': today,
            })
        new_relation = relation_obj.search([
            ('this_partner_id', '=', self.new_parent_id.id),
            ('other_partner_id', '=', self.partner_id.id)])
        if new_relation:
            new_relation.write({
                'date_start': today,
                'date_end': False,
            })
        else:
            relation_obj.create({
                'this_partner_id': self.new_parent_id.id,
                'type_selection_id': reltypesel.id,
                'other_partner_id': self.partner_id.id,
                'date_start': today,
            })
        self.partner_id.with_context(change_parent=True).write({
            'parent_id': self.new_parent_id.id,
        })
        return True
