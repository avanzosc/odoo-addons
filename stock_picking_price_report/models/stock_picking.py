# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        compute="_compute_currency_id",
        store=True,
        copy=False,
    )
    amount_total = fields.Monetary(
        string="Amount total",
        compute="_compute_amount_total",
        currency_field="currency_id",
    )

    @api.depends(
        "move_ids", "move_ids.sale_line_id", "move_ids.sale_line_id.currency_id"
    )
    def _compute_currency_id(self):
        for picking in self:
            currency = self.env["res.currency"]
            lines = picking.move_ids.filtered(lambda x: x.sale_line_id)
            for line in lines:
                currency = line.sale_line_id.currency_id
            if not currency:
                currency = picking.company_id.currency_id
            picking.currency_id = currency.id

    def _compute_amount_total(self):
        for picking in self:
            amount_total = 0
            lines = picking.move_line_ids.filtered(
                lambda x: x.state == "done"
                and x.move_id
                and x.qty_done
                and (x.move_id.sale_line_id or x.move_id.purchase_line_id)
            )
            for line in lines:
                price_unit = 0
                if line.move_id.sale_line_id:
                    price_unit = line.move_id.sale_line_id.price_unit
                if line.move_id.purchase_line_id:
                    price_unit = line.move_id.purchase_line_id.price_unit
                amount = line.qty_done * price_unit
                amount_total += amount
            picking.amount_total = amount_total
