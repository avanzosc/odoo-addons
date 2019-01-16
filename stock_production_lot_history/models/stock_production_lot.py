# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _


class StockProductionLotStatus(models.Model):
    _name = 'stock.production.lot.status'
    _description = 'Lot status'

    name = fields.Char(string='Status', required=True, translate=True)

    @api.multi
    def unlink(self):
        status = self.env.ref(
            'stock_production_lot_history.first_lot_status', False)
        s = self.filtered(lambda c: c.id == status.id)
        if s:
            raise exceptions.Warning(
                _('You can not delete the first status of lots.'))
        return super(StockProductionLotStatus, self).unlink()


class StockProductionLotHistoricalStates(models.Model):
    _name = 'stock.production.lot.historical.states'
    _description = 'Lot historical states'
    _rec_name = 'date'
    _order = "lot_id, date desc"

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot', required=True)
    lot_status_id = fields.Many2one(
        comodel_name='stock.production.lot.status', string='Lot status',
        required=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='User', required=True)
    date = fields.Datetime(string="Date", required=True)
    reason = fields.Text(string="Motive", required=True)
    reference = fields.Char(string="reference")


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    lot_status_id = fields.Many2one(
        comodel_name='stock.production.lot.status', string='Lot status')
    historical_states_ids = fields.One2many(
        comodel_name='stock.production.lot.historical.states',
        inverse_name='lot_id', string='Historical states')

    @api.model
    def create(self, values):
        status = self.env.ref(
            'stock_production_lot_history.first_lot_status', False)
        values['lot_status_id'] = status.id
        return super(StockProductionLot, self).create(values)

    @api.multi
    def _change_lot_state(self, status, reason, reference):
        for lot in self:
            lot.write({'lot_status_id': status.id})
            historical_vals = ({'lot_id': lot.id,
                                'lot_status_id': status.id,
                                'user_id': self.env.uid,
                                'date': fields.Datetime.now(),
                                'reason': reason,
                                'reference': reference})
            self.env['stock.production.lot.historical.states'].create(
                historical_vals)
