# -*- coding: utf-8 -*-
# Copyright © 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizChangeLotState(models.TransientModel):
    _name = 'wiz.change.lot.state'

    lot_status_id = fields.Many2one(
        comodel_name='stock.production.lot.status', string='Lot status',
        required=True)
    reason = fields.Text(string="Motive", required=True)
    reference = fields.Char(string="reference")

    @api.multi
    def change_lot_state(self):
        self.ensure_one()
        lots = self.env['stock.production.lot'].browse(
            self.env.context.get('active_ids'))
        lots._change_lot_state(self.lot_status_id, self.reason, self.reference)
