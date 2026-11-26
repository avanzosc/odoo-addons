# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    is_repair = fields.Boolean(
        string="It's repair", store=True, copy=False, related="picking_id.is_repair"
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="stock_move_repair_account_tax_rel",
        column1="move_id",
        column2="tax_id",
        domain=[("type_tax_use", "=", "sale")],
        check_company=True,
        copy=False,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        digits="Product Price",
        compute="_compute_price_subtotal",
        store=True,
        copy=False,
    )
    price_tax = fields.Float(
        string="Tax Amount",
        digits="Product Price",
        compute="_compute_price_subtotal",
        store=True,
        copy=False,
    )

    @api.depends(
        "product_uom_qty", "quantity", "price_unit", "tax_ids", "repair_id.state"
    )
    def _compute_price_subtotal(self):
        for move in self:
            if not move.repair_id:
                move.price_subtotal = 0.0
                move.price_tax = 0.0
                continue
            qty = (
                move.quantity
                if move.repair_id.state == "done"
                else move.product_uom_qty
            )
            amounts = move.tax_ids.compute_all(
                move.price_unit,
                currency=move.company_id.currency_id,
                quantity=qty,
                product=move.product_id,
                partner=move.repair_id.partner_id,
            )
            move.price_subtotal = amounts["total_excluded"]
            move.price_tax = amounts["total_included"] - amounts["total_excluded"]

    def _get_repair_sale_price(self):
        self.ensure_one()
        if self.repair_line_type != "add" or not self.product_id:
            return 0.0
        price_unit = self.product_id.lst_price
        if self.product_uom:
            price_unit = self.product_id.uom_id._compute_price(
                price_unit, self.product_uom
            )
        return price_unit

    def _get_repair_taxes(self):
        self.ensure_one()
        if self.repair_line_type != "add" or not self.product_id:
            return self.env["account.tax"]
        return self.repair_id._get_repair_product_taxes(self.product_id)

    @api.onchange("product_id", "product_uom", "repair_line_type")
    def _onchange_repair_price_unit(self):
        if self.repair_id.sale_id:
            self.price_unit = self._get_repair_sale_price()
            self.tax_ids = self._get_repair_taxes()

    def find_or_create_from_repair(self, picking):
        move = self.search(
            [
                ("picking_id", "=", picking.id),
                ("state", "not in", ["cancel", "done"]),
                ("product_id", "=", self.product_id.id),
            ]
        )
        if move:
            move.write(
                {
                    "product_uom_qty": move.product_uom_qty + self.product_uom_qty,
                }
            )
        else:
            self.copy(
                default={
                    "repair_id": False,
                    "picking_id": picking.id,
                    "location_id": picking.location_id.id,
                    "location_dest_id": picking.location_dest_id.id,
                    "sale_line_id": self.repair_id.sale_line_id.id,
                }
            )
        return move

    # def _action_done(self, cancel_backorder=False):
    #     if self.env.context.get("move_no_to_done"):
    #         return self.env["stock.move"]
    #     else:
    #         return super(StockMove, self)._action_done(
    #             cancel_backorder=cancel_backorder
    #         )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "no_create_move_line" in self.env.context and "move_line_ids" in vals:
                del vals["move_line_ids"]
            if "default_origin_from_devolution" in self.env.context:
                vals["origin"] = self.env.context.get("default_origin_from_devolution")
        moves = super().create(vals_list)
        for move, vals in zip(moves, vals_list, strict=True):
            if not move.repair_id.sale_id:
                continue
            if "price_unit" not in vals:
                move.price_unit = move._get_repair_sale_price()
            if "tax_ids" not in vals:
                move.tax_ids = move._get_repair_taxes()
        moves._put_amount_untaxed_in_price_in_sale_budget()
        return moves

    def write(self, vals):
        result = super().write(vals)
        if "product_uom_qty" in vals or "price_unit" in vals:
            self._put_amount_untaxed_in_price_in_sale_budget()
        return result

    def _put_amount_untaxed_in_price_in_sale_budget(self):
        self.filtered(
            lambda x: x.repair_id and x.repair_line_type == "add"
        ).repair_id._put_amount_untaxed_in_price_in_sale_budget()

    def unlink(self):
        for move in self.filtered(
            lambda x: x.state == "draft"
            and x.repair_id
            and x.repair_id.from_repair_picking_out_id
            and x.repair_id.state != "cancel"
            and x.sale_line_id
        ):
            raise ValidationError(
                _(
                    "You cannot delete this movement, because it is associated "
                    "with repair: {}. Go ahead with the out picking, and then "
                    "report the units to be shipped."
                ).format(move.repair_id.name)
            )
        return super().unlink()
