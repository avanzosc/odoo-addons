# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class StockInformation(models.Model):
    _inherit = 'stock.information'

    @api.multi
    def _compute_week(self):
        super(StockInformation, self)._compute_week()
        p_obj = self.env['procurement.order']
        move_obj = self.env['stock.move']
        for line in self:
            if line.first_week:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], location_id=line.location,
                    periods=False)
            else:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], from_date=line.first_day_week,
                    location_id=line.location, periods=False)
            line.outgoing_pending_amount = sum(moves.mapped('product_uom_qty'))
            line.outgoing_pending_moves = [(6, 0, moves.ids)]
            states = ['confirmed', 'exception']
            if line.first_week:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    products=[line.product.id], location_id=line.location,
                    without_reserves=False, without_plan=False)
            else:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    from_date=line.first_day_week, products=[line.product.id],
                    location_id=line.location, without_reserves=False,
                    without_plan=False)
            line.outgoing_pending_amount_reserv = sum(
                procurements.mapped('product_qty'))
            line.outgoing_pending_procurement_reserv = (
                [(6, 0, procurements.ids)])
            line.outgoing_pending_amount_moves = line.outgoing_pending_amount
            line.outgoing_pending_amount += line.outgoing_pending_amount_reserv
            states = ['confirmed', 'exception']
            if line.first_week:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    products=[line.product.id], location_id=line.location,
                    without_reserves=True, without_plan=False)
            else:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    from_date=line.first_day_week, products=[line.product.id],
                    location_id=line.location, without_reserves=True,
                    without_plan=False)
            line.incoming_pending_amount_plan = sum(
                procurements.mapped('product_qty'))
            line.incoming_pending_procurements_plan = (
                [(6, 0, procurements.ids)])
            if line.first_week:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    products=[line.product.id], location_id=line.location,
                    without_reserves=False, without_plan=False)
            else:
                procurements = p_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    from_date=line.first_day_week, products=[line.product.id],
                    location_id=line.location, without_reserves=False,
                    without_plan=False)
            line.incoming_pending_amount_plan_reservation = sum(
                procurements.mapped('product_qty'))
            line.incoming_pending_procurements_plan_reservation = (
                [(6, 0, procurements.ids)])
            line.incoming_pending_amount += (
                line.incoming_pending_amount_plan +
                line.incoming_pending_amount_plan_reservation)
            line.stock_availability = (line.qty_available - line.minimum_rule +
                                       line.incoming_pending_amount)
            if line.stock_availability >= line.outgoing_pending_amount:
                line.virtual_stock = 0
            else:
                line.virtual_stock = (line.outgoing_pending_amount -
                                      line.stock_availability)

    incoming_pending_amount_plan = fields.Float(
        'Incoming pending amount from plan', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Incoming from plan')
    incoming_pending_procurements_plan = fields.Many2many(
        comodel_name='procurement.order',
        string='Incoming pending procurements from plan',
        relation='rel_stock_info_incoming_pending_procurement_plan',
        column1='stock_info_id', column2='pending_procurement_plan_id',
        compute='_compute_week')
    incoming_pending_amount_plan_reservation = fields.Float(
        'Incoming pending amount from plan reservation',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_week', help='Incoming from plan reservation')
    incoming_pending_procurements_plan_reservation = fields.Many2many(
        comodel_name='procurement.order',
        string='Incoming pending procurements from plan reservation',
        relation='rel_stock_info_incoming_pending_procurement_plan_reserv',
        column1='stock_info_id', column2='pending_procurement_plan_id',
        compute='_compute_week')
    outgoing_pending_amount_moves = fields.Float(
        'Outgoing pending amount from moves', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Gross requirement')
    outgoing_pending_amount_reserv = fields.Float(
        'Outgoing pending amount reservation', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Gross requirement reservation')
    outgoing_pending_procurement_reserv = fields.Many2many(
        comodel_name='procurement.order',
        string='Outgoing pending procurements reservation',
        relation='rel_stock_info_outgoing_pending_procurement_reserv',
        column1='stock_info_id', column2='pending_procurement_reserv_id',
        compute='_compute_week')

    @api.multi
    def show_outgoing_pending_reserved_moves(self):
        self.ensure_one()
        return {'name': _('Outgoing pending reserved procurements'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'procurement.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in',
                            self.outgoing_pending_procurement_reserv.ids)]}

    @api.multi
    def show_incoming_procurements_from_plan(self):
        self.ensure_one()
        return {'name': _('Incoming procurements from plan'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'procurement.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in',
                            self.incoming_pending_procurements_plan.ids)]}

    @api.multi
    def show_incoming_procurements_from_plan_reservation(self):
        self.ensure_one()
        ids = self.incoming_pending_procurements_plan_reservation.ids
        return {'name': _('Incoming procurements from plan reservation'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'procurement.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', ids)]}
