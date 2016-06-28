# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
from dateutil.relativedelta import relativedelta
import openerp.addons.decimal_precision as dp


class StockInformation(models.Model):
    _name = 'stock.information'
    _description = 'Stock information'
    _order = 'company, location, product, first_day_week asc'

    @api.multi
    def _compute_week(self):
        orderpoint_obj = self.env['stock.warehouse.orderpoint']
        proc_obj = self.env['procurement.order']
        move_obj = self.env['stock.move']
        pur_line_obj = self.env['purchase.order.line']
        sale_line_obj = self.env['sale.order.line']
        for line in self:
            line.qty_available = 0
            line.minimum_rule = 0
            if line.product and line.location:
                cond = [('company_id', '=', line.company.id),
                        ('product_id', '=', line.product.id),
                        ('location_id', '=', line.location.id),
                        ('active', '=', True)]
                rule = orderpoint_obj.search(cond, limit=1)
                if rule:
                    line.minimum_rule = rule.product_min_qty
                if line.first_week:
                    prod = self.env['product.product'].with_context(
                        {'location': line.location.id}).browse(line.product.id)
                    line.qty_available = prod.qty_available
                else:
                    year = line.year
                    week = line.week - 1
                    if line.week == 1:
                        year -= 1
                        new_date = str(year) + '-12-31'
                        new_date = fields.Datetime.from_string(new_date).date()
                        week = new_date.strftime('%W')
                    cond = [('company', '=', line.company.id),
                            ('year', '=', year),
                            ('week', '=', week),
                            ('location', '=', line.location.id),
                            ('product', '=', line.product.id)]
                    prev = self.search(cond, limit=1)
                    if (prev.stock_availability >=
                            prev.outgoing_pending_amount):
                        line.qty_available = (
                            prev.stock_availability + line.minimum_rule -
                            prev.outgoing_pending_amount)
                    else:
                        line.qty_available = line.minimum_rule
            if line.first_week:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], location_dest_id=line.location)
            else:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], from_date=line.first_day_week,
                    location_dest_id=line.location)
            line.incoming_pending_amount = sum(moves.mapped('product_uom_qty'))
            line.incoming_pending_moves = [(6, 0, moves.ids)]
            moves = moves.filtered(lambda x: x.purchase_line_id)
            purchase_orders = self.env['purchase.order']
            purchase_orders |= moves.mapped('purchase_line_id.order_id')
            line.incoming_pending_purchases = [(6, 0, purchase_orders.ids)]
            if line.first_week:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], location_id=line.location)
            else:
                moves = move_obj._find_moves_from_stock_information(
                    line.company, line.last_day_week,
                    products=[line.product.id], from_date=line.first_day_week,
                    location_id=line.location)
            line.outgoing_pending_amount = sum(moves.mapped('product_uom_qty'))
            line.outgoing_pending_moves = [(6, 0, moves.ids)]
            states = ['confirmed', 'exception']
            if line.first_week:
                procs = proc_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    products=[line.product.id], location_id=line.location)
            else:
                procs = proc_obj._find_procurements_from_stock_information(
                    line.company, line.last_day_week, states=states,
                    from_date=line.first_day_week, products=[line.product.id],
                    location_id=line.location)
            line.demand = sum(procs.mapped('product_qty'))
            procurement_orders = self.env['procurement.order']
            if procs:
                procurement_orders |= procs
            line.demand_procurements = [(6, 0, procurement_orders.ids)]
            if line.first_week:
                purchase_lines = (
                    pur_line_obj._find_purchase_lines_from_stock_information(
                        line.company, line.last_day_week, line.product,
                        line.location))
            else:
                purchase_lines = (
                    pur_line_obj._find_purchase_lines_from_stock_information(
                        line.company, line.last_day_week, line.product,
                        line.location, from_date=line.first_day_week))
            line.draft_purchases_amount = sum(
                purchase_lines.mapped('product_qty'))
            purchase_orders = self.env['purchase.order']
            if purchase_lines:
                purchase_orders |= purchase_lines.mapped('order_id')
            line.draft_purchases = [(6, 0, purchase_orders.ids)]
            if line.first_week:
                sale_lines = (
                    sale_line_obj._find_sale_lines_from_stock_information(
                        line.company, line.last_day_week, line.product,
                        line.location))
            else:
                sale_lines = (
                    sale_line_obj._find_sale_lines_from_stock_information(
                        line.company, line.last_day_week, line.product,
                        line.location, from_date=line.first_day_week))
            line.draft_sales_amount = sum(sale_lines.mapped('product_uom_qty'))
            sale_orders = self.env['sale.order']
            if sale_lines:
                sale_orders |= sale_lines.mapped('order_id')
            line.draft_sales = [(6, 0, sale_orders.ids)]
            line.stock_availability = (line.qty_available - line.minimum_rule +
                                       line.incoming_pending_amount)
            if line.stock_availability >= line.outgoing_pending_amount:
                line.virtual_stock = 0
            else:
                line.virtual_stock = (line.outgoing_pending_amount -
                                      line.stock_availability)

    @api.multi
    @api.depends('product', 'product.seller_ids')
    def _compute_product_info(self):
        for line in self:
            sequence = False
            for supplier in line.product.seller_ids:
                if not sequence or sequence and sequence > supplier.sequence:
                    sequence = supplier.sequence
                    line.supplier = supplier.name.id

    company = fields.Many2one(
        comodel_name='res.company', string='Company', select=True)
    year = fields.Integer(string='Year', select=True)
    week = fields.Integer(string='Week', select=True)
    first_week = fields.Boolean(
        string='First week', default=False)
    first_day_week = fields.Date(string='First day on week')
    last_day_week = fields.Date(string='Last day on week')
    location = fields.Many2one(
        comodel_name='stock.location', string='Location', translate=True,
        select=True)
    product = fields.Many2one(
        comodel_name='product.product', string='Product', translate=True,
        select=True)
    category = fields.Many2one(
        comodel_name='product.category', string='category', store=True,
        related='product.categ_id')
    product_template = fields.Many2one(
        comodel_name='product.template', string='Product template', store=True,
        related='product.product_tmpl_id')
    route = fields.Many2one(
        'stock.location.route', 'Product Type')
    supplier = fields.Many2one(
        'res.partner', 'Supplier', compute='_compute_product_info',
        store=True)
    qty_available = fields.Float(
        string='Quantity On Hand', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Initial stock')
    minimum_rule = fields.Float(
        string='Minimum rule', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Minimum rule')
    incoming_pending_amount = fields.Float(
        'Incoming pending amount', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Incoming pending')
    incoming_pending_purchases = fields.Many2many(
        comodel_name='purchase.order',
        relation='rel_stock_info_incoming_pending_purchase',
        column1='stock_info_id', column2='purchase_id',
        string='Purchases', compute='_compute_week')
    incoming_pending_moves = fields.Many2many(
        comodel_name='stock.move', string='Moves incoming to date',
        relation='rel_stock_info_incoming_pending_move',
        column1='stock_info_id', column2='move_in_id', compute='_compute_week')
    stock_availability = fields.Float(
        'Stock availability (DPS)', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Stock availability')
    demand = fields.Float(
        'Demand (D)', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Demand')
    demand_procurements = fields.Many2many(
        comodel_name='procurement.order', string='Demand procurements',
        relation='rel_stock_info_demand_procurement', compute='_compute_week',
        column1='stock_info_id', column2='proc_id')
    draft_purchases_amount = fields.Float(
        'Draft purchases amount (INFO)', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Draft purchases amount')
    draft_purchases = fields.Many2many(
        comodel_name='purchase.order', string='Draft purchases',
        relation='rel_stock_info_draft_purchase', compute='_compute_week',
        column1='stock_info_id', column2='purchase_id')
    draft_sales_amount = fields.Float(
        'Draft sales amount (INFO)', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Draft sales amount')
    draft_sales = fields.Many2many(
        comodel_name='sale.order', string='Draft sales',
        relation='rel_stock_draft_sale', compute='_compute_week',
        column1='stock_info_id', column2='sale_id')
    outgoing_pending_amount = fields.Float(
        'Outgoing pending amount', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Gross requirement')
    outgoing_pending_moves = fields.Many2many(
        comodel_name='stock.move', string='Moves outgoing to date',
        relation='rel_stock_info_outgoing_pending_moves',
        column1='stock_info_id', column2='move_out_id',
        compute='_compute_week')
    virtual_stock = fields.Float(
        'Virtual stock', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Net requirement')

    def _calculate_first_day_week(self, date):
        found = False
        if date.weekday() == 0 or (date.day == 1 and date.month == 1):
            found = True
        while not found:
            date = date + relativedelta(days=-1)
            if date.weekday() == 0 or (date.day == 1 and date.month == 1):
                found = True
        return date.strftime('%Y-%m-%d')

    def _calculate_last_day_week(self, date):
        found = False
        if date.weekday() == 6 or (date.day == 31 and date.month == 12):
            found = True
        while not found:
            date = date + relativedelta(days=+1)
            if date.weekday() == 6 or (date.day == 31 and date.month == 12):
                found = True
        return date.strftime('%Y-%m-%d')

    def _generate_stock_information(self, wiz, product_datas):
        buy_route = self.env.ref('purchase.route_warehouse0_buy')
        for data in product_datas:
            datos_array = product_datas[data]
            from_date = fields.Date.context_today(self)
            from_date = self._calculate_first_day_week(
                fields.Datetime.from_string(from_date).date())
            from_date = fields.Date.from_string(from_date)
            to_date = self._calculate_last_day_week(
                fields.Datetime.from_string(wiz.to_date).date())
            to_date = fields.Date.from_string(to_date)
            first_week = True
            while from_date <= to_date:
                first = self._calculate_first_day_week(from_date)
                last = self._calculate_last_day_week(from_date)
                route_id = False
                if (datos_array['product'].route_ids and buy_route.id in
                        datos_array['product'].route_ids.ids):
                    route_id = buy_route.id
                vals = {'company': wiz.company.id,
                        'location': datos_array['location'].id,
                        'product': datos_array['product'].id,
                        'route': route_id,
                        'year': from_date.year,
                        'week': from_date.strftime('%W'),
                        'first_day_week': first,
                        'last_day_week': last,
                        'first_week': first_week}
                if first_week:
                    vals['first_day_week'] = fields.Date.context_today(self)
                    first_week = False
                self.create(vals)
                from_date = fields.Date.to_string(from_date +
                                                  relativedelta(days=7))
                from_date = fields.Date.from_string(from_date)

    @api.multi
    def show_incoming_pending_purchases(self):
        self.ensure_one()
        return {'name': _('Purchase orders'),
                'view_type': 'form',
                "view_mode": 'tree,form,graph,calendar',
                'res_model': 'purchase.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.incoming_pending_purchases.ids)]}

    @api.multi
    def show_incoming_pending_moves(self):
        self.ensure_one()
        return {'name': _('Incoming pending stock moves'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'stock.move',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.incoming_pending_moves.ids)]}

    @api.multi
    def show_outgoing_pending_moves(self):
        self.ensure_one()
        return {'name': _('Outgoing pending stock moves'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'stock.move',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.outgoing_pending_moves.ids)]}

    @api.multi
    def show_demand_procurements(self):
        self.ensure_one()
        return {'name': _('Procurement orders in draft state'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'procurement.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.demand_procurements.ids)]}

    @api.multi
    def show_draft_purchases(self):
        self.ensure_one()
        return {'name': _('Purchase orders in draft state'),
                'view_type': 'form',
                "view_mode": 'tree,form,graph,calendar',
                'res_model': 'purchase.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.draft_purchases.ids)]}

    @api.multi
    def show_draft_sales(self):
        self.ensure_one()
        return {'name': _('Sale orders in draft state'),
                'view_type': 'form',
                "view_mode": 'tree,form,calendar,graph',
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.draft_sales.ids)]}
