# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    parent_picking_id = fields.Many2one(comodel_name="stock.picking",
                                        string="Parent Picking")

    @api.multi
    def create_complementary_picking(self, location_id=False):
        picking_lines = []
        picking_type = self.env['stock.picking.type'].search(
            [("code", "=", "internal")], limit=1)
        for line in self.move_ids_without_package:
            comp_qty = line.reserved_availability - line.quantity_done
            if comp_qty:
                picking_lines.append((0, 0, {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': comp_qty,
                    'product_uom': line.product_uom.id,
                })
                                     )
        return self.create({
            'origin': self.name,
            'picking_type_id': picking_type.id,
            'move_ids_without_package': picking_lines,
            'parent_picking_id': self.id,
            'group_id': self.group_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'location_dest_id': self.location_dest_id.id,
            'location_id': location_id and location_id.id
            or self.location_id.id,
        })
