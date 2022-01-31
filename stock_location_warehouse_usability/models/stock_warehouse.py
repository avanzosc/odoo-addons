# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def _compute_location_count(self):
        for warehouse in self:
            warehouse.location_count = len(warehouse.location_ids)

    street = fields.Char(
        string='Street',
        related='partner_id.street',
        store=True)
    street2 = fields.Char(
        string='Street 2',
        related='partner_id.street2',
        store=True)
    city = fields.Char(
        string='City',
        related='partner_id.city',
        store=True)
    state_id = fields.Many2one(
        string='State',
        comodel_name='res.country.state',
        related='partner_id.state_id',
        store=True)
    zip = fields.Char(
        string='Zip',
        related='partner_id.zip',
        store=True)
    country_id = fields.Many2one(
        string='Country',
        comodel_name='res.country',
        related='partner_id.country_id',
        store=True)
    location_ids = fields.One2many(
        string='Locations',
        comodel_name='stock.location',
        inverse_name='warehouse_id')
    location_count = fields.Integer(
        '# Locations', compute='_compute_location_count')

    def action_view_location(self):
        context = self.env.context.copy()
        context.update({'default_warehouse_id': self.id})
        return {
            'name': _("Locations"),
            'view_mode': 'tree,form',
            'res_model': 'stock.location',
            'domain': [('id', 'in', self.location_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
