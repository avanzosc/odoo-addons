# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    picking_id = fields.Many2one(
        string='Transfer', comodel_name='stock.picking')
    max_weight = fields.Float(
        string='Maximum Weight', related='packaging_id.max_weight', store=True)
    pack_length = fields.Float(string='Pack Length')
    width = fields.Float(string='Pack Width')
    height = fields.Float(string='Pack Height')
    partner_id = fields.Many2one(
        string='Delivery Address', comodel_name='res.partner',
        related='picking_id.partner_id', store=True)

    @api.onchange('packaging_id')
    def onchange_dimension(self):
        if self.packaging_id.height:
            self.height = self.packaging_id.height
        if self.packaging_id.width:
            self.width = self.packaging_id.width
        if self.packaging_id.packaging_length:
            self.pack_length = self.packaging_id.packaging_length
        if self.packaging_id.length_uom_id:
            self.length_uom_id = self.packaging_id.length_uom_id.id
        if self.packaging_id.volume_uom_id:
            self.volume_uom_id = self.packaging_id.volume_uom_id.id
        if self.packaging_id.weight_uom_id:
            self.weight_uom_id = self.packaging_id.weight_uom_id.id
        if self.packaging_id.volume:
            self.volume = self.packaging_id.volume

    @api.model
    def create(self, vals):
        line = super(StockQuantPackage, self).create(vals)
        line.name = u'{} {} {}{}'.format(line.picking_id.name, '-', '00', len(
                line.picking_id.quant_package_ids))
        return line
