# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _compute_warehouse_count(self):
        for partner in self:
            partner.warehouse_count = len(partner.warehouse_ids)

    warehouse_ids = fields.One2many(
        string='Warehouses', comodel_name='stock.warehouse',
        inverse_name='farmer_id')
    warehouse_count = fields.Integer(
        '# Warehouses', compute='_compute_warehouse_count')

    def action_view_warehouse(self):
        context = self.env.context.copy()
        context.update({'default_partner_id': self.id})
        return {
            'name': _("Warehouses"),
            'view_mode': 'tree,form',
            'res_model': 'stock.warehouse',
            'domain': [('id', 'in', self.warehouse_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
