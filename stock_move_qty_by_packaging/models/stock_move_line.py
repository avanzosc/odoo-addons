# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _compute_boxes_sacs(self):
        for line in self:
            if line.picking_id.state != "done":
                qty = line.reserved_uom_qty
            else:
                qty = line.qty_done
            boxes_sacks = 0
            if (
                line.move_id
                and line.move_id.sale_line_id
                and line.move_id.sale_line_id.product_packaging_qty
            ):
                sale_line = line.move_id.sale_line_id
                packaging_qty = sale_line.product_packaging_qty
                product_uom_qty = sale_line.product_uom_qty
                boxes_sacks = (qty * packaging_qty) / product_uom_qty
            line.boxes_sacks = boxes_sacks

    boxes_sacks = fields.Integer(string="Boxes/Sacks", compute="_compute_boxes_sacs")
    product_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        string="Packaging",
        domain="[('product_id','=',product_id)]",
        check_company=True,
    )
    product_packaging_qty = fields.Float(string="Packaging Quantity")
    palet_id = fields.Many2one(
        string="Palet",
        comodel_name="product.packaging",
        copy=False,
        domain="[('is_generic', '=', True)]",
    )
    palet_qty = fields.Float(
        string="Contained Palet Quantity", digits="Product Unit of Measure", copy=False
    )
    no_update_palet_qty = fields.Boolean(string="No update palet_qty", default=False)
    gross_weight = fields.Float(string="Gross Weight")

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        out_picking_lines = self.filtered(lambda x: x.picking_code == "outgoing")
        if not result or len(self) != len(out_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self.filtered(
                lambda x: x.move_id
                and x.qty_done
                and x.move_id.sale_line_id
                and x.sale_line_id.product_packaging_qty
            ):
                line_key = self._generate_key_to_found()
                if line_key == clave:
                    boxes_sacks = move_line._get_boxes_sacks()
                    result[line_key]["boxes_sacks"] = boxes_sacks
        return result

    def _generate_keys_to_found(self):
        uom = self.product_uom_id
        name = self.product_id.display_name
        description = self.move_id.description_picking
        product = self.product_id
        if description == name or description == self.product_id.name:
            description = False
        line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
        return line_key

    def _get_boxes_sacks(self):
        sale_line = self.sale_line_id
        packaging_qty = sale_line.product_packaging_qty
        product_uom_qty = sale_line.product_uom_qty
        uom = self.product_uom_id
        qty_done = self.product_uom_id._compute_quantity(self.qty_done, uom)
        boxes_sacks = (qty_done * packaging_qty) / product_uom_qty
        return boxes_sacks

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        self.no_update_palet_qty = True
        if self.product_packaging_id:
            self.product_packaging_qty = 1
            self.qty_done = self.product_packaging_id.qty
            if self.product_packaging_id.palet_id:
                self.palet_id = self.product_packaging_id.palet_id.id
            else:
                self.palet_id = False
                self.palet_qty = 0
        if self.palet_id and self.qty_done:
            self.palet_qty = self._get_palet_qty()
            self.no_update_palet_qty = False
        else:
            self.product_packaging_qty = 0
            self.qty_done = 1
            self.palet_id = False
            self.palet_qty = 0

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        self.no_update_palet_qty = True
        if self.product_packaging_id and self.product_packaging_qty:
            self.qty_done = self.product_packaging_qty * self.product_packaging_id.qty
        if self.palet_id and self.qty_done:
            self.palet_qty = self._get_palet_qty()
            self.no_update_palet_qty = False

    @api.onchange("gross_weight")
    def _onchange_gross_weight(self):
        weight_categ = self.env.ref("uom.product_uom_categ_kgm")
        qty_done = self.gross_weight
        if self.gross_weight and self.product_uom_id.category_id == weight_categ:
            if (
                self.product_packaging_id
                and self.product_packaging_id.weight
                and self.product_packaging_qty
            ):
                qty_done -= (
                    self.product_packaging_id.weight * self.product_packaging_qty
                )
            if self.palet_id and self.palet_id.weight and self.palet_qty:
                qty_done -= self.palet_id.weight * self.palet_qty
        self.qty_done = qty_done

    def _get_palet_qty(self):
        return self.qty_done / (
            self.product_packaging_id.qty * self.product_packaging_id.palet_qty
        )

    @api.onchange("palet_qty")
    def _onchange_palet_qty(self):
        if (
            not self.no_update_palet_qty
            and self.product_id
            and self.product_packaging_id
            and self.palet_id
            and self.product_id.packaging_ids
            and self.palet_qty
        ):
            line = self.product_id.packaging_ids.filtered(
                lambda x: x.name
                and x.palet_id
                and x.name == self.product_packaging_id.name
                and x.palet_id == self.palet_id
            )
            if line and len(line) == 1:
                self.product_packaging_qty = self.palet_qty * line.palet_qty
        elif self.no_update_palet_qty:
            self.no_update_palet_qty = False
