# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    reader = fields.Char(string="Reader", copy=False)

    @api.onchange("reader")
    def onchange_reader(self):
        if self.reader:
            pos = self.reader.find(" ")
            cond = [("default_code", "=", self.reader)]
            if pos > 0:
                default_code = self.reader[0:pos]
                cond = [("default_code", "=", default_code)]
            product = self.env["product.product"].search(cond, limit=1)
            if not product:
                raise ValidationError(
                    _("Product not found, reader information: {}").format(self.reader)
                )
            stock_move = self.picking_id.move_ids_without_package.filtered(
                lambda x: x.product_id == product
            )
            if not stock_move:
                raise ValidationError(
                    _("Reader product: {}, not found.").format(product.name)
                )
            self.product_id = product.id
            if pos > 0:
                name = self.reader[pos + 1 : len(self.reader)]
                cond = [("name", "=", name), ("product_id", "=", product.id)]
                lot = self.env["stock.lot"].search(cond, limit=1)
                if not lot:
                    raise ValidationError(
                        _(
                            "Lot: {}, for product: {} not found. Reader "
                            "information: {}"
                        ).format(name, product.name, self.reader)
                    )
                self.lot_id = lot.id
                self.move_id = stock_move.id

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if (
                "reader" in values
                and values.get("reader", False)
                and "move_id" in values
                and values.get("move_id", False)
                and "product_id" not in values
            ):
                move = self.env["stock.move"].browse(values.get("move_id", False))
                values["product_id"] = move.product_id.id
        lines = super().create(vals_list)
        return lines
