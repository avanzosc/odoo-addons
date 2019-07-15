# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    relocate = fields.Boolean(string='Relocate', default=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _compute_show_relocation_button(self):
        for picking in self:
            picking.show_relocation_button = True
            if (picking.relocation_made or picking.location_dest_id.usage !=
                'internal' or picking.state != 'done' or not
                    picking.picking_type_id.relocate):
                picking.show_relocation_button = False

    relocation_made = fields.Boolean(string='Relocation made', default=False)
    show_relocation_button = fields.Boolean(
        string='Show relocation button',
        compute='_compute_show_relocation_button')

    @api.multi
    def button_relocate(self):
        self.ensure_one()
        wiz_obj = self.env['stock.quant.move']
        quants = self.move_lines.filtered(
            lambda x: x.state == 'done').mapped('quant_ids')
        wiz = wiz_obj.with_context(
            {'active_ids': quants.ids,
             'active_model': 'stock.quant',
             'picking_id': self.id}).create({})
        context = self.env.context.copy()
        context.update({
            'active_ids': quants.ids,
            'active_model': 'stock.quant'})
        return {'name': _('Quants'),
                'type': 'ir.actions.act_window',
                'res_model': 'stock.quant.move',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                'context': context}
