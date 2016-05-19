# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class StockInformation(models.Model):
    _inherit = 'stock.information'

    @api.multi
    def _compute_week(self):
        prod_obj = self.env['mrp.production']
        super(StockInformation, self)._compute_week()
        for line in self:
            moves = line.incoming_pending_moves.filtered(
                lambda x: not x.purchase_line_id and not x.production_id)
            line.incoming_pending_amount_moves = sum(
                moves.mapped('product_uom_qty'))
            moves = line.incoming_pending_moves.filtered(
                lambda x: x.purchase_line_id)
            line.incoming_pending_amount_purchases = sum(
                moves.mapped('product_uom_qty'))
            moves = line.incoming_pending_moves.filtered(
                lambda x: x.production_id)
            line.incoming_pending_amount_productions = sum(
                moves.mapped('product_uom_qty'))
            productions = self.env['mrp.production']
            productions |= moves.mapped('production_id')
            line.incoming_pending_productions = [(6, 0, productions.ids)]
            draft_prods = prod_obj._find_productions_from_stock_information(
                line.company, line.last_day_week, line.product, line.location,
                state=['draft'], from_date=line.first_day_week)
            line.draft_productions_amount = sum(
                draft_prods.mapped('product_qty'))
            line.draft_productions = [(6, 0, draft_prods.ids)]

    incoming_pending_amount_moves = fields.Float(
        'Incoming pending amount moves', compute='_compute_week',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    incoming_pending_amount_purchases = fields.Float(
        'Incoming pending amount purchases', compute='_compute_week',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    incoming_pending_amount_productions = fields.Float(
        'Incoming pending amount productions', compute='_compute_week',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    incoming_pending_productions = fields.Many2many(
        comodel_name='mrp.production',
        relation='rel_stock_info_mrp_production',
        column1='stock_info_id', column2='production_id',
        string='MRP Productions', compute='_compute_week')
    draft_productions_amount = fields.Float(
        'Draft productions amount (INFO)', compute='_compute_week',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    draft_productions = fields.Many2many(
        comodel_name='mrp.production', string='Draft productions',
        relation='rel_stock_info_production', compute='_compute_week',
        column1='stock_info_id', column2='sale_id')

    @api.multi
    def show_incoming_pending_productions(self):
        self.ensure_one()
        return {'name': _('MRP productions'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.incoming_pending_productions.ids)]
                }

    @api.multi
    def show_draft_productions(self):
        self.ensure_one()
        return {'name': _('MRP draft productions'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.draft_productions.ids)]}
