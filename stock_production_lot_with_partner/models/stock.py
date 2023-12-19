# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    customer_id = fields.Many2one(
        string='Customer', comodel_name='res.partner')
    supplier_id = fields.Many2one(
        string='Supplier', comodel_name='res.partner')
    observations = fields.Text(
        string='Observations')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, vals):
        line = super(StockMoveLine, self).create(vals)
        if 'lot_id' in vals and vals.get('lot_id', False):
            if (line.picking_id and
                line.picking_id.picking_type_id.code == 'incoming' and
                    line.lot_id.id == vals.get('lot_id')):
                if not line.lot_id.supplier_id:
                    line.lot_id.supplier_id = line.picking_id.partner_id.id
        return line

    @api.multi
    def write(self, vals):
        result = super(StockMoveLine, self).write(vals)
        if 'lot_id' in vals and vals.get('lot_id', False):
            for line in self.filtered(
                    lambda x: x.picking_id and
                    x.picking_id.picking_type_id.code == 'incoming' and
                    x.lot_id.id == vals.get('lot_id')):
                if not line.lot_id.supplier_id:
                    line.lot_id.supplier_id = line.picking_id.partner_id.id
        return result


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_done(self):
        result = super(StockPicking, self).action_done()
        for picking in self.filtered(
            lambda x: x.picking_type_id and
                x.picking_type_id.code == 'outgoing'):
            for line in picking.move_line_ids.filtered(lambda x: x.lot_id):
                if (picking.picking_type_id.code == 'outgoing' and not
                        line.lot_id.customer_id):
                    line.lot_id.customer_id = line.picking_id.partner_id.id
        return result
