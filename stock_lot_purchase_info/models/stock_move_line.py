# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    supplier_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        copy=False,
        store=True,
        related="lot_id.supplier_id",
    )
    purchase_price = fields.Float(
        string="Purchase Price Unit",
        digits="Product Price",
        copy=False,
        store=True,
        related="lot_id.purchase_price",
    )
    def _action_done(self):
        return super(StockMoveLine, self.with_context(
            from_action_done=True))._action_done()

    def write(self, vals):
        result = super(StockMoveLine, self).write(vals)
        if "from_action_done" in self.env.context:
            for line in self.filtered(
                    lambda ml: ml.lot_id and ml.move_id.purchase_line_id):
                lot_vals = {}
                pl = line.move_id.purchase_line_id
                if line.lot_id.purchase_price != pl.price_unit:
                    lot_vals["purchase_price"] = pl.price_unit
                if line.lot_id.supplier_id != pl.order_id.partner_id:
                    lot_vals["supplier_id"] = pl.order_id.partner_id.id
                if lot_vals:
                    line.lot_id.write(lot_vals)
        return result
