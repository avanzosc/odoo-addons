# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    parent_picking_id = fields.Many2one(comodel_name="stock.picking",
                                        string="Parent Picking")
    complementary_pickings_count = fields.Integer(
        string="Complementary Count", compute="compute_complementary_pickings")

    @api.multi
    def compute_complementary_pickings(self):
        for picking in self:
            picking.complementary_pickings_count = picking.search_count([(
                'parent_picking_id', '=', picking.id)])

    @api.multi
    def create_complementary_picking(self, location_id=False):
        complementary_pickings = []
        picking_type = self.env['stock.picking.type'].search(
            [("code", "=", "internal")], limit=1)
        for picking in self:
            picking_lines = []
            for line in picking.move_ids_without_package:
                comp_qty = line.product_uom_qty - line.reserved_availability
                if comp_qty:
                    picking_lines.append((0, 0, {
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': comp_qty,
                        'product_uom': line.product_uom.id,
                    }))
            complementary_pickings.append((picking, picking.create({
                'origin': picking.name,
                'picking_type_id': picking_type.id,
                'move_ids_without_package': picking_lines,
                'parent_picking_id': picking.id,
                'group_id': picking.group_id.id,
                'partner_id': picking.partner_id.id,
                'company_id': picking.company_id.id,
                'location_dest_id': picking.location_id.id,
                'location_id': (location_id and location_id.id
                                or picking.location_id.id),
            })))
        return complementary_pickings
