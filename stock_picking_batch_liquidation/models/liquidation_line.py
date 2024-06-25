# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class LiquidationLine(models.Model):
    _name = "liquidation.line"
    _description = "Liquidation Line"

    batch_id = fields.Many2one(string="Batch", comodel_name="stock.picking.batch")
    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", required=True
    )
    unit = fields.Float(string="Units")
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Price", digits="Standard Cost Decimal Precision")
    amount = fields.Float(string="Amount")
    amount_charge = fields.Float(string="Amount Charge")
    amount_pay = fields.Float(string="Amount Pay")
    type = fields.Selection(
        string="Type",
        selection=[("charge", "Charge"), ("pay", "Pay"), ("variable", "Variable")],
    )

    @api.onchange("batch_id")
    def onchange_product_domain(self):
        domain = {}
        self.ensure_one()
        if (
            self.batch_id
            and (self.batch_id.liquidation_contract_id)
            and (self.batch_id.liquidation_contract_id.contract_line_ids)
        ):
            product = []
            done_product = []
            done_lines = self.batch_id.liquidation_line_ids
            for done in done_lines:
                if done.product_id.id not in done_product:
                    done_product.append(done.product_id.id)
            for line in self.batch_id.liquidation_contract_id.contract_line_ids:
                if (
                    line.product_id.id not in (product)
                    and (line.product_id.id) not in done_product
                ):
                    product.append(line.product_id.id)
            domain = {"domain": {"product_id": [("id", "in", product)]}}
        return domain

    @api.onchange("product_id")
    def onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            unit = 0
            quantity = 0
            amount = 0
            price = 0
            n = 1
            contract = self.batch_id.liquidation_contract_id
            contract_line = contract.contract_line_ids.filtered(
                lambda c: c.product_id == self.product_id
            )
            if len(contract_line) == 1:
                movelines = self.batch_id.move_line_ids.filtered(
                    lambda c: c.move_type_id == contract_line.move_type_id
                    and c.state == "done"
                )
                if contract_line.quantity_type == "unit" and movelines:
                    unit = sum(movelines.mapped("download_unit"))
                if contract_line.quantity_type == "kg" and movelines:
                    quantity = sum(movelines.mapped("qty_done"))
                if contract_line.quantity_type == "fixed":
                    quantity = 1
                if contract_line.price_type == "feed":
                    price = self.batch_id.feed_price
                if contract_line.price_type == "correction":
                    price = self.batch_id.amount
                if contract_line.price_type == "contract":
                    price = contract_line.price
                if (
                    contract_line.price_type == "average"
                    and (movelines)
                    and sum(movelines.mapped("qty_done")) != 0
                ):
                    price = sum(movelines.mapped("amount")) / sum(
                        movelines.mapped("qty_done")
                    )
                if contract_line.type == "charge":
                    n = -1
                if contract_line.type == "variable":
                    dif = self.batch_id.difference
                    if dif < 0:
                        n = -1
                if quantity != 0:
                    amount = n * quantity * price
                if unit != 0:
                    amount = n * unit * price
                self.unit = unit
                self.quantity = quantity
                self.price = price
                self.amount = amount
                self.type = contract_line.type
                self.onchange_amount()

    @api.onchange("unit", "quantity", "price", "type")
    def onchange_unit(self):
        self.ensure_one()
        n = 1
        amount = self.amount
        if self.type == "charge":
            n = -1
        if self.type == "variable":
            if self.batch_id.difference < 0:
                n = -1
        if self.unit:
            amount = n * self.unit * self.price
        if self.quantity:
            amount = n * self.quantity * self.price
        self.amount = amount

    @api.onchange("amount")
    def onchange_amount(self):
        self.ensure_one()
        if self.amount > 0:
            amount_pay = self.amount
            amount_charge = 0
        else:
            amount_charge = abs(self.amount)
            amount_pay = 0
        self.amount_pay = amount_pay
        self.amount_charge = amount_charge
