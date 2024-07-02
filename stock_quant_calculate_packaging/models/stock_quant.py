# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.tools import float_round


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        string="Packaging",
        check_company=True,
        compute="_compute_product_packaging_info",
        store=True,
        copy=False,
    )
    product_packaging_qty = fields.Float(
        string="Packages",
        compute="_compute_product_packaging_info",
        store=True,
        copy=False,
    )
    new_product_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        string="New Packaging",
        check_company=True,
        copy=False,
    )
    new_product_packaging_qty = fields.Float(
        string="New amount of packages",
        copy=False,
    )

    @api.depends(
        "quantity",
        "new_product_packaging_id",
        "product_id",
        "product_id.packaging_ids",
        "product_id.packaging_ids.qty",
    )
    def _compute_product_packaging_info(self):
        for quant in self:
            packaging = False
            packaging_qty = 0
            if quant.new_product_packaging_id:
                packaging = quant.new_product_packaging_id
            else:
                if quant.product_id and quant.product_id.packaging_ids:
                    packaging = quant.product_id.packaging_ids[0]
            if packaging:
                packaging_uom = packaging.product_uom_id
                packaging_uom_qty = quant.product_uom_id._compute_quantity(
                    quant.quantity, packaging_uom
                )
                packaging_qty = float_round(
                    packaging_uom_qty / packaging.qty,
                    precision_rounding=packaging_uom.rounding,
                )
            quant.product_packaging_qty = packaging_qty
            quant.product_packaging_id = packaging.id if packaging else False

    @api.onchange("new_product_packaging_id")
    def _onchange_new_product_packaging_id(self):
        if self.new_product_packaging_id:
            self.new_product_packaging_qty = 1
            self.inventory_quantity = self.new_product_packaging_id.qty
        else:
            self.new_product_packaging_qty = 0
            self.inventory_quantity = 1

    @api.onchange("new_product_packaging_qty")
    def _onchange_new_product_packaging_qty(self):
        if self.new_product_packaging_id and self.new_product_packaging_qty:
            self.inventory_quantity = (
                self.new_product_packaging_qty * self.new_product_packaging_id.qty
            )

    @api.onchange("inventory_quantity")
    def _onchange_product_uom_qty(self):
        if self.new_product_packaging_id and self.inventory_quantity:
            packaging_uom = self.new_product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom_id._compute_quantity(
                self.inventory_quantity, packaging_uom
            )
            self.new_product_packaging_qty = float_round(
                packaging_uom_qty / self.new_product_packaging_id.qty,
                precision_rounding=packaging_uom.rounding,
            )

    def action_set_inventory_quantity_to_zero(self):
        result = super().action_set_inventory_quantity_to_zero()
        self.new_product_packaging_qty = 0
        return result

    @api.model
    def _get_inventory_fields_write(self):
        fields = super()._get_inventory_fields_write()
        fields += ["new_product_packaging_id", "new_product_packaging_qty"]
        return fields
