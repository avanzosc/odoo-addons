# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    make_id = fields.Many2one(string="Make", comodel_name="product.make")
    allowed_make_ids = fields.Many2many(
        string="Allowed makes", comodel_name="product.make"
    )
    market_id = fields.Many2one(
        string="Market",
        comodel_name="res.partner.market",
        related="picking_id.market_id",
        store=True,
    )
    market_sector_id = fields.Many2one(
        string="Market sector",
        comodel_name="res.partner.market.sector",
        related="picking_id.market_sector_id",
        store=True,
    )

    def _get_new_picking_values(self):
        result = super()._get_new_picking_values()
        if "origin" in result and result.get("origin", False):
            cond = [("name", "=", result.get("origin"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale and sale.commercial_make_id:
                result["commercial_make_id"] = sale.commercial_make_id.id
            if sale and sale.allowed_commercial_make_ids:
                result["allowed_commercial_make_ids"] = [
                    (6, 0, sale.allowed_commercial_make_ids.ids)
                ]
            if sale and sale.num_allowed_commercial_make:
                result["num_allowed_commercial_make"] = sale.num_allowed_commercial_make
            if sale and sale.team_id:
                result["team_id"] = sale.team_id.id
        return result

    @api.onchange("product_id")
    def onchange_product_id(self):
        result = super().onchange_product_id()
        if not self.product_id or (
            self.product_id and not self.product_id.product_make_ids
        ):
            return result
        if self.partner_id or self.picking_partner_id:
            self.put_makes_in_line()
        return result

    def put_makes_in_line(self):
        commercial_make = False
        if "commercial_make_id" in self.env.context:
            if not self.env.context.get("commercial_make_id", False):
                raise exceptions.ValidationError(
                    _(" You must select a commercial make on the picking.")
                )
            commercial_make = self.env["product.make"].browse(
                self.env.context.get("commercial_make_id")
            )
        else:
            if self.picking_id.commercial_make_id:
                commercial_make = self.picking.commercial_make_id
        if self.picking_id.picking_type_code != "outgoing":
            self.picking_id.commercial_make_id = False
            self.picking_id.allowed_commercial_make_ids = [(6, 0, [])]
            self.picking_id.num_allowed_commercial_make = 0
            return
        if commercial_make:
            found = False
            for product_make in self.product_id.product_tmpl_id.product_make_ids:
                if commercial_make == product_make:
                    self.allowed_make_ids = [(6, 0, product_make.ids)]
                    self.make_id = product_make.id
                    found = True
            if not found:
                raise exceptions.ValidationError(
                    _("The product: %(product)s, does not have the make: %(make)s.")
                    % {"product": self.product_id.name, "make": commercial_make.name}
                )

    @api.model_create_multi
    def create(self, values_list):
        moves = self.env["stock.move"]
        for values in values_list:
            if "sale_line_id" in values and values.get("sale_line_id", False):
                line = self.env["sale.order.line"].browse(values.get("sale_line_id"))
                if line and line.make_id:
                    values["make_id"] = line.make_id.id
                if line and line.allowed_make_ids:
                    values["allowed_make_ids"] = [(6, 0, line.allowed_make_ids.ids)]
            move = super().create(values)
            if "sale_line_id" not in values and move.picking_id:
                if not move.make_id:
                    move.put_makes_in_line()

            moves += move
        # moves._update_orderpoints()
        for move in moves:
            move.picking_id.update_division_in_pickings()
        return moves
