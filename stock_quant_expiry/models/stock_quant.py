# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    @api.multi
    @api.depends('lot_id.life_date', 'lot_id.mrp_date')
    def _compute_lifespan(self):
        for record in self.filtered(lambda x: x.lot_id and
                                    x.lot_id.life_date and x.lot_id.mrp_date):
            life_date = fields.Date.from_string(record.lot_id.life_date)
            mrp_date = fields.Date.from_string(record.lot_id.mrp_date)
            record.lifespan = (life_date - mrp_date).days

    def _compute_lifespan_progress(self):
        for record in self.filtered(lambda x: x.lot_id and
                                    x.lot_id.life_date and x.lot_id.mrp_date):
            life_date = fields.Date.from_string(record.lot_id.life_date)
            mrp_date = fields.Date.from_string(record.lot_id.mrp_date)
            today = fields.Date.from_string(fields.Date.today())
            lifespan = (life_date - mrp_date).days
            todayspan = (today - mrp_date).days
            if not lifespan:
                continue
            record.lifespan_progress = float(todayspan) / float(lifespan) * 100

    mrp_date = fields.Date(string='Mrp Date', store=True,
                           related='lot_id.mrp_date')
    life_date = fields.Datetime(string='Expiry Date',
                                related='lot_id.life_date')
    lifespan = fields.Integer(string='Lifespan', store=True,
                              compute='_compute_lifespan')
    lifespan_progress = fields.Float(string='Lifespan Progress',
                                     compute='_compute_lifespan_progress')
