# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.tools.safe_eval import safe_eval
from dateutil.relativedelta import relativedelta

LIMIT_2_FIELD = {
    1: 'alert_date',
    2: 'removal_date',
    3: 'use_date',
    }


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    @api.onchange('mrp_date', 'life_date')
    @api.multi
    def onchange_mrp_life_date(self):
        self.ensure_one()
        if not self.mrp_date or not self.life_date:
            return {}
        stock_config_model = self.env['stock.config.settings']
        mrp_date = fields.Date.from_string(self.mrp_date)
        life_date = fields.Date.from_string(self.life_date)
        lifespan = (life_date - mrp_date).days
        vals = stock_config_model.get_default_stock_lot_percentage([])
        variation1 = lifespan * vals.get('stock_lot_percentage1', 0) / 100
        variation2 = lifespan * vals.get('stock_lot_percentage2', 0) / 100
        variation3 = lifespan * vals.get('stock_lot_percentage3', 0) / 100
        self.alert_date = mrp_date + relativedelta(days=variation1)
        self.removal_date = mrp_date + relativedelta(days=variation2)
        self.use_date = mrp_date + relativedelta(days=variation3)

    @api.multi
    @api.depends('life_date', 'mrp_date')
    def _compute_lifespan(self):
        for record in self.filtered(lambda x: x.life_date and x.mrp_date):
            life_date = fields.Date.from_string(record.life_date)
            mrp_date = fields.Date.from_string(record.mrp_date)
            record.lifespan = (life_date - mrp_date).days

    def _compute_lifespan_progress(self):
        for record in self.filtered(lambda x: x.life_date and x.mrp_date):
            life_date = fields.Date.from_string(record.life_date)
            mrp_date = fields.Date.from_string(record.mrp_date)
            today = fields.Date.from_string(fields.Date.today())
            lifespan = (life_date - mrp_date).days
            todayspan = (today - mrp_date).days
            if not lifespan:
                continue
            record.lifespan_progress = float(todayspan) / float(lifespan) * 100

    lifespan = fields.Integer(string='Lifespan', store=True,
                              compute='_compute_lifespan')
    lifespan_progress = fields.Float(string='Lifespan Progress',
                                     compute='_compute_lifespan_progress')
    qty_available = fields.Float(
        compute='_compute_product_available',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Quantity On Hand',
        search='_search_product_qty_available',
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    virtual_available = fields.Float(
        compute='_compute_product_available',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Forecast Quantity',
        search='_search_product_virtual_available',
        help="Forecast quantity (computed as Quantity On Hand "
             "- Outgoing + Incoming)\n"
             "In a context with a single Stock Location, this includes "
             "goods stored in this location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    incoming_qty = fields.Float(
        compute='_compute_product_available',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Incoming',
        search='_search_product_incoming_qty',
        help="Quantity of products that are planned to arrive.\n"
             "In a context with a single Stock Location, this includes "
             "goods arriving to this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods arriving to the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods arriving to any Stock "
             "Location with 'internal' type.")
    outgoing_qty = fields.Float(
        compute='_compute_product_available',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Outgoing',
        search='_search_product_outgoing_qty',
        help="Quantity of products that are planned to leave.\n"
             "In a context with a single Stock Location, this includes "
             "goods leaving this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods leaving the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods leaving any Stock "
             "Location with 'internal' type.")

    @api.depends('product_id')
    def _compute_product_available(self):
        for lot in self:
            lot.qty_available = lot.product_id.with_context(
                lot_id=lot.id).qty_available
            lot.virtual_available = lot.product_id.with_context(
                lot_id=lot.id).virtual_available
            lot.incoming_qty = lot.product_id.with_context(
                lot_id=lot.id).incoming_qty
            lot.outgoing_qty = lot.product_id.with_context(
                lot_id=lot.id).outgoing_qty

    @api.multi
    def _search_product_qty_available(self, operator, value):
        domain = []
        lot_ids = []
        for lot in self.search([]):
            if safe_eval(str(lot['qty_available']) + operator + str(value)):
                lot_ids.append(lot.id)
        domain.append(('id', 'in', lot_ids))
        return domain

    @api.multi
    def _search_product_virtual_available(self, operator, value):
        domain = []
        lot_ids = []
        for lot in self.search([]):
            if safe_eval(
                    str(lot['virtual_available']) + operator + str(value)):
                lot_ids.append(lot.id)
        domain.append(('id', 'in', lot_ids))
        return domain

    @api.multi
    def _search_product_incoming_qty(self, operator, value):
        domain = []
        lot_ids = []
        for lot in self.search([]):
            if safe_eval(str(lot['incoming_qty']) + operator + str(value)):
                lot_ids.append(lot.id)
        domain.append(('id', 'in', lot_ids))
        return domain

    @api.multi
    def _search_product_outgoing_qty(self, operator, value):
        domain = []
        lot_ids = []
        for lot in self.search([]):
            if safe_eval(str(lot['outgoing_qty']) + operator + str(value)):
                lot_ids.append(lot.id)
        domain.append(('id', 'in', lot_ids))
        return domain

    @api.multi
    def get_lots_by_limit(self, day, limit=None):
        body_msg = ''
        if not limit:
            return body_msg
        day = fields.Datetime.from_string(day)
        start_day = fields.Datetime.to_string(
            day.replace(hour=0, minute=0, second=0))
        end_day = fields.Datetime.to_string(
            day.replace(hour=23, minute=59, second=59))
        domain = [(LIMIT_2_FIELD.get(limit), '>=', start_day),
                  (LIMIT_2_FIELD.get(limit), '<=', end_day)]
        for lot in self.search(domain):
            body_msg_tmpl = (
                "<small><strong>Lot: </strong>{}   <strong>Internal Ref: "
                "</strong>{}   <strong>Product:</strong> [{}] {}<br/></small>")
            body_msg += body_msg_tmpl.format(
                lot.name, lot.ref, lot.product_id.default_code,
                lot.product_id.name)
        return body_msg

    @api.multi
    def send_mail(self, email_to):
        mail_obj = self.env['mail.mail']
        stock_config_model = self.env['stock.config.settings']
        today = fields.Date.today()
        vals = stock_config_model.get_default_stock_lot_percentage([])
        limit1 = vals.get('stock_lot_percentage1', 0)
        limit2 = vals.get('stock_lot_percentage2', 0)
        limit3 = vals.get('stock_lot_percentage3', 0)
        body_tmpl = ("Some lots had exceeded the limits defined in their "
                     "lifespan {}:<br/><br/><strong>1st Limit: {}%<br/>"
                     "</strong>{}<br/><strong>2nd Limit: {}%<br/></strong>{}"
                     "<br/><strong>3rd Limit: {}%<br/></strong>{}")
        body = body_tmpl.format(today, limit1,
                                self.get_lots_by_limit(today, 1),
                                limit2, self.get_lots_by_limit(today, 2),
                                limit3, self.get_lots_by_limit(today, 3))
        values = {
            'subject': 'Lot Limits exceeded: {}'.format(today),
            'body': body,
            'body_html': body,
            'email_to': email_to,
        }
        mail = mail_obj.create(values)
        mail.send()
