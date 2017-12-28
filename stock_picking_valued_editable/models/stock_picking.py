# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    valued = fields.Boolean(string='Valued', related=False, readonly=False)

    @api.onchange('partner_id')
    def onchange_partner_id_valued(self):
        self.ensure_one()
        self.valued = self.partner_id.valued_picking

    @api.model
    def create(self, values):
        if values.get('partner_id', False):
            partner = self.env['res.partner'].browse(values.get('partner_id'))
            values.update({'valued': partner.valued_picking})
        return super(StockPicking, self).create(values)
