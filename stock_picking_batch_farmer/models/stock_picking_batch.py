# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickinBatch(models.Model):
    _inherit = "stock.picking.batch"

    farmer_id = fields.Many2one(
        string='Farmer',
        comodel_name='res.partner',
        related='warehouse_id.farmer_id',
        store=True)
    tax_entity_id = fields.Many2one(
        string='Tax Entity',
        comodel_name='res.partner',
        related='warehouse_id.tax_entity_id',
        store=True)
    operating_number = fields.Char(
        related='location_id.warehouse_id.farm_numexp',
        store=True)
    picking_count = fields.Integer(
        '# Transfers',
        compute='_compute_picking_count')
    move_count = fields.Integer(
        '# Stock Moves',
        compute='_compute_move_count')
    move_line_count = fields.Integer(
        '# Stock Move Lines',
        compute='_compute_move_line_count')

    def _compute_picking_count(self):
        for batch in self:
            batch.picking_count = len(batch.picking_ids)

    def _compute_move_count(self):
        for batch in self:
            batch.move_count = len(batch.move_ids)

    def _compute_move_line_count(self):
        for batch in self:
            batch.move_line_count = len(batch.move_line_ids)

    def action_view_picking(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        context.update({'search_default_group_catogory_type': 1})
        if 'search_default_draft' in context:
            context.update({'search_default_draft': False})
        return {
            'name': _("Transfers"),
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', self.picking_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    def action_view_move(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        context.update({'search_default_group_catogory_type': 1})
        return {
            'name': _("Stock Moves"),
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'domain': [('id', 'in', self.move_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }

    def action_view_move_line(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        context.update({'search_default_group_catogory_type': 1})
        return {
            'name': _("Stock Move Lines"),
            'view_mode': 'tree,form',
            'res_model': 'stock.move.line',
            'domain': [('id', 'in', self.move_line_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
