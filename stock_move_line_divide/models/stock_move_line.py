# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    divide = fields.Integer(string="Divide in", default=1)

    def action_divide(self):
        self.ensure_one()
        if self.divide != 0:
            divide = self.divide
            qty = self.reserved_uom_qty or self.qty_done
            packaging_qty = self.product_packaging_qty
            qty_assign = qty // divide
            qty_pack_assign = packaging_qty // divide
            rest = qty % divide
            self.write(
                {
                    "reserved_uom_qty": qty_assign,
                    "qty_done": qty_assign,
                    "product_packaging_qty": qty_pack_assign,
                }
            )
            package_type = self.packaging_id.id
            self.picking_id._put_in_pack(self, create_package_level=True)
            self.packaging_id = package_type
            vals = {
                "product_id": self.product_id.id,
                "location_id": self.location_id.id,
                "location_dest_id": self.location_dest_id.id,
                "lot_id": self.lot_id.id,
                "reserved_uom_qty": qty_assign,
                "lot_name": self.lot_name,
                "product_uom_id": self.product_uom_id.id,
                "package_id": self.package_id.id,
                "product_packaging_id": self.product_packaging_id.id,
                "product_packaging_qty": qty_pack_assign,
            }
            for _record in range(1, divide):
                line = self.env["stock.move.line"].create(vals)
                line.picking_id._put_in_pack(line, create_package_level=True)
                line.packaging_id = package_type
            if rest != 0:
                vals["reserved_uom_qty"] = rest
                line = self.env["stock.move.line"].create(vals)
                line.picking_id._put_in_pack(line, create_package_level=True)
                line.packaging_id = package_type
            self.divide = 1
        elif self.qty_done != 0:
            qty = self.reserved_uom_qty or self.qty_done
            qty_assign = qty // self.qty_done
            rest = qty % self.qty_done
            self.write(
                {
                    "reserved_uom_qty": self.qty_done,
                }
            )
            package_type = self.packaging_id.id
            self.picking_id._put_in_pack(self, create_package_level=True)
            self.packaging_id = package_type
            vals = {
                "product_id": self.product_id.id,
                "location_id": self.location_id.id,
                "location_dest_id": self.location_dest_id.id,
                "lot_id": self.lot_id.id,
                "reserved_uom_qty": self.qty_done,
                "product_uom_id": self.product_uom_id.id,
                "package_id": self.package_id.id,
                "product_packaging_id": self.product_packaging_id.id,
                "product_packaging_qty": self.product_packaging_qty,
            }
            for _record in range(1, int(qty_assign)):
                line = self.env["stock.move.line"].create(vals)
                line.picking_id._put_in_pack(line, create_package_level=True)
                line.packaging_id = package_type
            if rest != 0:
                vals["reserved_uom_qty"] = rest
                line = self.env["stock.move.line"].create(vals)
                line.picking_id._put_in_pack(line, create_package_level=True)
                line.packaging_id = package_type
        else:
            raise ValidationError(
                _("The dividing amount or done quantity can not be 0.")
            )
